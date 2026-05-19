"""DAG Airflow — pipeline météo Maroc (Medallion)."""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "4IASDG2",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_morocco_pipeline",
    default_args=default_args,
    description="Pipeline météo 8 villes Maroc — Bronze/Silver/Gold",
    schedule_interval="0 6 * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "maroc", "weather"],
) as dag:
    ingestion_bronze = BashOperator(
        task_id="ingestion_bronze",
        bash_command="python /opt/airflow/scripts/bronze_ingestion.py",
    )

    test_bronze_task = BashOperator(
        task_id="test_bronze",
        bash_command="python /opt/airflow/scripts/data_quality.py --layer bronze",
    )

    transform_silver = BashOperator(
        task_id="transform_silver",
        bash_command="python /opt/airflow/scripts/silver_transform.py",
    )

    test_silver_task = BashOperator(
        task_id="test_silver",
        bash_command="python /opt/airflow/scripts/data_quality.py --layer silver",
    )

    enrich_gold_task = BashOperator(
        task_id="enrich_gold",
        bash_command="python /opt/airflow/scripts/gold_enrich.py",
    )

    test_gold_task = BashOperator(
        task_id="test_gold",
        bash_command="python /opt/airflow/scripts/data_quality.py --layer gold",
    )

    (
        ingestion_bronze
        >> test_bronze_task
        >> transform_silver
        >> test_silver_task
        >> enrich_gold_task
        >> test_gold_task
    )
