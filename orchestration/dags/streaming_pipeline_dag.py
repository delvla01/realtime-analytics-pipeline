from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'clickstream_processing',
    default_args=default_args,
    description='Process clickstream data from Kafka to PostgreSQL',
    schedule_interval=None,
    start_date=datetime(2024, 5, 14),
    catchup=False,
) as dag:
    
    # Use PostgresOperator to create database and table
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_default',
        sql='''
        CREATE TABLE IF NOT EXISTS clickstream_events (
            user_id BIGINT,
            event_type VARCHAR(255),
            timestamp DOUBLE PRECISION,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''',
        database='analytics',
    )

    # Use BashOperator to run Spark job locally
    process_clickstream = BashOperator(
        task_id='process_clickstream_data',
        bash_command="""
        cd /opt/airflow/realtime-analytics-pipeline && 
        /opt/spark/bin/spark-submit \
          --master local[*] \
          --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.postgresql:postgresql:42.5.1 \
          /opt/airflow/realtime-analytics-pipeline/streaming/process_stream.py 60
        """,
    )

    # Task to verify data
    verify_data = PostgresOperator(
        task_id='verify_data',
        postgres_conn_id='postgres_default',
        sql='''
        SELECT COUNT(*) FROM clickstream_events;
        ''',
        database='analytics',
    )

    # Define dependencies
    create_table >> process_clickstream >> verify_data