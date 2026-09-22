import ast, json
from pathlib import Path
from deltalake import DeltaTable

ROOT=Path(__file__).resolve().parents[1]

def test_incremental_checkpoint_covers_sources():
    checkpoint=json.loads((ROOT/"lakehouse/checkpoints/ingested_files.json").read_text())
    assert set(checkpoint)=={p.name for p in (ROOT/"data/source").glob("*.csv")}

def test_bronze_and_silver_are_real_delta_tables():
    for name in ["customers","accounts","transactions","loans","fraud_cases"]:
        assert DeltaTable(str(ROOT/"lakehouse/bronze"/name)).version() >= 0
        assert DeltaTable(str(ROOT/"lakehouse/silver"/name)).version() >= 0

def test_airflow_dag_source_and_dependencies_are_valid():
    text=(ROOT/"airflow/dags/fintrust_daily_pipeline.py").read_text()
    ast.parse(text)
    assert "ingest_source >> bronze_quality >> silver_transform >> silver_quality >> dbt_gold" in text

def test_tier3_validation_artifacts_pass():
    assert json.loads((ROOT/"validation/tier3_quality.json").read_text())["status"]=="PASS"
    assert json.loads((ROOT/"validation/tier3_kpi_reconciliation.json").read_text())["status"]=="PASS"
    assert json.loads((ROOT/"validation/dbt_build_summary.json").read_text())["status"]=="PASS"
