"""Executable local lakehouse pipeline, portable to ADLS and Databricks."""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, sys, uuid
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
import pandas as pd
import pyarrow.dataset as ds
from deltalake import DeltaTable, write_deltalake

ROOT = Path(__file__).resolve().parents[1]
SOURCE, LAKE = ROOT / "data" / "source", ROOT / "lakehouse"
CHECKPOINT = LAKE / "checkpoints" / "ingested_files.json"
RUN_LOG = ROOT / "monitoring" / "pipeline_runs.jsonl"
KEYS = {"customers":"customer_id","accounts":"account_id","transactions":"transaction_id","loans":"loan_id","loan_payments":"payment_id","branches":"branch_id","cards":"card_id","fraud_cases":"case_id","interactions":"interaction_id","monthly_balances":"balance_snapshot_id"}

def now(): return datetime.now(timezone.utc).isoformat()
def checksum(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""): h.update(block)
    return h.hexdigest()
def log(record):
    RUN_LOG.parent.mkdir(parents=True,exist_ok=True)
    with RUN_LOG.open("a",encoding="utf-8") as f: f.write(json.dumps(record,default=str)+"\n")

def ingest(run_id):
    CHECKPOINT.parent.mkdir(parents=True,exist_ok=True)
    state=json.loads(CHECKPOINT.read_text()) if CHECKPOINT.exists() else {}
    rows=skipped=0; batch_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for src in sorted(SOURCE.glob("*.csv")):
        digest=checksum(src)
        if state.get(src.name)==digest: skipped+=1; continue
        landing=LAKE/"landing"/batch_id; landing.mkdir(parents=True,exist_ok=True); shutil.copy2(src,landing/src.name)
        frame=pd.read_csv(src); frame["_source_filename"]=src.name; frame["_batch_id"]=batch_id; frame["_ingested_at"]=now()
        target=LAKE/"bronze"/src.stem
        write_deltalake(str(target),frame,mode="append" if target.exists() else "overwrite",schema_mode="merge")
        rows+=len(frame); state[src.name]=digest
    CHECKPOINT.write_text(json.dumps(state,indent=2),encoding="utf-8")
    return {"rows_written":rows,"files_skipped":skipped,"batch_id":batch_id}

def spark_transform(run_id):
    from pyspark.sql import SparkSession, functions as F
    os.environ["PYSPARK_PYTHON"]=sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"]=sys.executable
    spark=(SparkSession.builder.master("local[2]").appName("FinTrustTier3")
           .config("spark.sql.session.timeZone","UTC").config("spark.pyspark.python",sys.executable)
           .config("spark.pyspark.driver.python",sys.executable).getOrCreate())
    spark.sparkContext.setLogLevel("ERROR"); written=0
    try:
        for name,key in KEYS.items():
            sdf=(spark.read.option("header",True).option("inferSchema",True).csv(str(SOURCE/f"{name}.csv"))
                 .dropDuplicates([key]).withColumn("_processed_at",F.current_timestamp()))
            if name=="transactions":
                sdf=(sdf.withColumn("transaction_ts",F.to_timestamp("transaction_ts")).filter(F.col("amount")>=0)
                     .withColumn("transaction_date",F.to_date("transaction_ts")).withColumn("transaction_year",F.year("transaction_ts"))
                     .withColumn("transaction_month",F.month("transaction_ts")).withColumn("risk_band",F.when(F.col("risk_score")>=.72,"High").when(F.col("risk_score")>=.4,"Medium").otherwise("Low")))
            elif name=="customers": sdf=sdf.withColumn("occupation_segment",F.initcap(F.trim("occupation_segment")))
            out=LAKE/"silver_parquet"/name
            if out.exists(): shutil.rmtree(out)
            writer=sdf.write.mode("overwrite")
            if name=="transactions": writer=writer.partitionBy("transaction_year","transaction_month")
            writer.parquet(str(out))
            clean=ds.dataset(str(out),format="parquet",partitioning="hive" if name=="transactions" else None).to_table(); delta=LAKE/"silver"/name
            if name=="transactions" and delta.exists(): shutil.rmtree(delta)
            write_deltalake(str(delta),clean,mode="overwrite",schema_mode="overwrite",
                            partition_by=["transaction_year","transaction_month"] if name=="transactions" else None)
            written+=clean.num_rows
    finally: spark.stop()
    return {"rows_written":written,"tables":len(KEYS)}

def quality():
    errors=[]; counts={}
    for name,key in KEYS.items():
        bronze=DeltaTable(str(LAKE/"bronze"/name)).to_pyarrow_table().to_pandas(); silver=DeltaTable(str(LAKE/"silver"/name)).to_pyarrow_table().to_pandas()
        counts[name]={"bronze":len(bronze),"silver":len(silver)}
        if silver[key].isna().any(): errors.append(f"{name}.{key} contains nulls")
        if silver[key].duplicated().any(): errors.append(f"{name}.{key} is not unique")
        if len(silver)>len(bronze): errors.append(f"{name} Silver exceeds Bronze")
    tx=DeltaTable(str(LAKE/"silver"/"transactions")).to_pyarrow_table().to_pandas()
    if (tx["amount"]<0).any(): errors.append("negative transaction amount")
    result={"status":"PASS" if not errors else "FAIL","errors":errors,"counts":counts}
    (ROOT/"validation"/"tier3_quality.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    if errors: raise ValueError("; ".join(errors))
    return result

def run():
    run_id=str(uuid.uuid4()); t0=perf_counter(); record={"run_id":run_id,"start_time":now(),"status":"RUNNING"}
    try:
        record["ingestion"]=ingest(run_id); record["silver"]=spark_transform(run_id); record["quality"]=quality()["status"]; record["status"]="SUCCESS"
    except Exception as exc: record.update(status="FAILED",failure_reason=repr(exc)); raise
    finally: record.update(end_time=now(),duration_seconds=round(perf_counter()-t0,3)); log(record); print(json.dumps(record,indent=2))

if __name__=="__main__":
    parser=argparse.ArgumentParser(); parser.add_argument("command",choices=["run","ingest","silver","quality"],default="run",nargs="?"); args=parser.parse_args()
    if args.command=="run": run()
    elif args.command=="ingest": print(json.dumps(ingest(str(uuid.uuid4())),indent=2))
    elif args.command=="silver": print(json.dumps(spark_transform(str(uuid.uuid4())),indent=2))
    else: print(json.dumps(quality(),indent=2))
