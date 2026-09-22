"""Tier-3 gates and KPI reconciliation for CI and Airflow."""
import argparse, ast, json
from pathlib import Path
import duckdb
from deltalake import DeltaTable
ROOT=Path(__file__).resolve().parents[1]; LAKE=ROOT/"lakehouse"
BASELINE={"customers":5000,"loan_outstanding":902482733.03,"dpd30_ratio":.1517,"dpd90_ratio":.0593,"digital_share":.6221,"high_risk_rate":.0002,"churn_rate":.0532}
def bronze():
    tables=sorted(p.name for p in (LAKE/"bronze").iterdir() if p.is_dir()); assert len(tables)==10,tables
    assert all(DeltaTable(str(LAKE/"bronze"/t)).version()>=0 for t in tables); return {"tables":tables}
def serving():
    db=LAKE/"serving"/"fintrust.duckdb"; assert db.exists(); con=duckdb.connect(str(db),read_only=True)
    actual=set(r[0] for r in con.execute("select table_name from information_schema.tables where table_schema='main'").fetchall())
    required={"dim_customer","dim_account","fact_transactions","fact_fraud","fact_risk"}; assert required<=actual,(required-actual)
    return {"tables":sorted(actual)}
def reconcile():
    con=duckdb.connect(str(LAKE/"serving"/"fintrust.duckdb"),read_only=True)
    results={"customers":con.execute("select count(*) from dim_customer").fetchone()[0],"loan_outstanding":float(con.execute("select sum(outstanding_amount) from fact_risk").fetchone()[0]),"dpd30_ratio":float(con.execute("select sum(case when days_past_due>=30 then outstanding_amount else 0 end)/sum(outstanding_amount) from fact_risk").fetchone()[0]),"dpd90_ratio":float(con.execute("select sum(case when days_past_due>=90 then outstanding_amount else 0 end)/sum(outstanding_amount) from fact_risk").fetchone()[0]),"digital_share":float(con.execute("select avg(case when channel in ('Mobile Banking','Internet Banking','UPI') then 1.0 else 0 end) from fact_transactions").fetchone()[0]),"high_risk_rate":float(con.execute("select avg(is_high_risk) from fact_transactions").fetchone()[0]),"churn_rate":float(con.execute("select avg(is_churned) from dim_customer").fetchone()[0])}
    tolerances={"customers":0,"loan_outstanding":1,"dpd30_ratio":.0005,"dpd90_ratio":.0005,"digital_share":.0005,"high_risk_rate":.0001,"churn_rate":.0005}
    for k,v in results.items(): assert abs(v-BASELINE[k])<=tolerances[k],(k,v,BASELINE[k])
    (ROOT/"validation"/"tier3_kpi_reconciliation.json").write_text(json.dumps({"status":"PASS","actual":results,"baseline":BASELINE},indent=2)); return results
def airflow_graph():
    path=ROOT/"airflow"/"dags"/"fintrust_daily_pipeline.py"; ast.parse(path.read_text()); text=path.read_text()
    expected=["ingest_source","bronze_quality_check","silver_transform","silver_quality_check","dbt_gold_models","dbt_docs","pipeline_reconciliation","publish_serving_layer"]
    assert all(x in text for x in expected); return {"tasks":expected,"parse":"PASS"}
def main(stage):
    out={}
    if stage in ("bronze","all"): out["bronze"]=bronze()
    if stage in ("serving","all"): out["serving"]=serving()
    if stage=="all": out["kpis"]=reconcile(); out["airflow"]=airflow_graph()
    print(json.dumps({"status":"PASS",**out},indent=2))
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("--stage",choices=["bronze","serving","all"],default="all"); main(p.parse_args().stage)
