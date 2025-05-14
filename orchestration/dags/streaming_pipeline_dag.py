from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="streaming_clickstream_pipeline",
    default_args=default_args,
    description="Simulates clickstream events, processes them with Spark, models them with dbt",
    schedule_interval=None,  # Manually triggered or use '@hourly' / cron
    start_date=datetime(2024, 1, 1),
    catchup=False,
) as dag:

    # Step 1: Start Kafka event producer
    simulate_events = BashOperator(
        task_id="simulate_clickstream_events",
        bash_command="""
        echo "Running clickstream event producer";
        python /opt/airflow/realtime-analytics-pipeline/simulation/event_producer.py || exit 1
        """,
    )

    # Step 2: Start Spark streaming job
    process_stream = BashOperator(
        task_id="process_stream_with_spark",
        bash_command="""
        docker exec spark spark-submit \
        --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,org.postgresql:postgresql:42.2.18 \
        /opt/bitnami/spark/project/streaming/process_stream.py
        """,
    )

    # Step 3: Run dbt transformations
    run_dbt = BashOperator(
        task_id="run_dbt_models",
        cwd="/opt/airflow/realtime-analytics-pipeline/warehouse",
        bash_command="dbt run",
    )

    # Step 4: Run dbt tests
    test_dbt = BashOperator(
        task_id="test_dbt_models",
        cwd="/opt/airflow/realtime-analytics-pipeline/warehouse",
        bash_command="dbt test",
    )

    simulate_events >> process_stream >> run_dbt >> test_dbt
