"""Reference Airflow DAG; commands remain idempotent and environment-configurable."""
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="fintrust_daily_analytics",
    start_date=datetime(2026, 1, 1),
    schedule="0 3 * * *",
    catchup=False,
    default_args={"owner":"analytics-engineering", "retries":2},
    tags=["banking", "portfolio"],
) as dag:
    generate = BashOperator(task_id="generate_source_extract", bash_command="python src/generate_data.py --scale demo")
    validate = BashOperator(task_id="validate_source_data", bash_command="python src/validate_data.py")
    dbt_build = BashOperator(task_id="build_warehouse_models", bash_command="cd dbt/fintrust && dbt build")
    generate >> validate >> dbt_build

