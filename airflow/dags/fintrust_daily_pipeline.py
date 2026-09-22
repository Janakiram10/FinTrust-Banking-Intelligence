"""Production-shaped FinTrust DAG; commands are idempotent and fail closed."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

DEFAULTS = {"owner": "analytics-engineering", "retries": 2, "retry_delay": timedelta(minutes=5)}
with DAG(dag_id="fintrust_lakehouse_daily", start_date=datetime(2026,1,1), schedule="0 3 * * *",
         catchup=False, max_active_runs=1, default_args=DEFAULTS,
         tags=["banking","lakehouse","quality-gated"]) as dag:
    ingest_source = BashOperator(task_id="ingest_source", bash_command="python lakehouse/pipeline.py ingest")
    bronze_quality = BashOperator(task_id="bronze_quality_check", bash_command="python tools/tier3_validate.py --stage bronze")
    silver_transform = BashOperator(task_id="silver_transform", bash_command="python lakehouse/pipeline.py silver")
    silver_quality = BashOperator(task_id="silver_quality_check", bash_command="python lakehouse/pipeline.py quality")
    dbt_gold = BashOperator(task_id="dbt_gold_models", bash_command="cd dbt/fintrust && dbt build --profiles-dir .")
    dbt_docs = BashOperator(task_id="dbt_docs", bash_command="cd dbt/fintrust && dbt docs generate --profiles-dir .")
    reconcile = BashOperator(task_id="pipeline_reconciliation", bash_command="python tools/tier3_validate.py --stage all")
    publish = BashOperator(task_id="publish_serving_layer", bash_command="python tools/tier3_validate.py --stage serving")
    ingest_source >> bronze_quality >> silver_transform >> silver_quality >> dbt_gold >> dbt_docs >> reconcile >> publish

