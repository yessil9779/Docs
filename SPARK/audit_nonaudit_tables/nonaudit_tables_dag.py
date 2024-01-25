from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(datetime.now().year, datetime.now().month, datetime.now().day),
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'nonaudit_tables_dag',
    default_args=default_args,
    description='Non Audit Tables DAG',
    schedule_interval=timedelta(days=1)
)

spark_nonaudit_path = '/opt/airflow/dags/spark_scripts/audit_nonaudit_tables/src/spark_nonaudit.py'

spark_nonaudit_task = SparkSubmitOperator(
    task_id='spark_nonaudit_task',
    conn_id='spark_remote',  # specify your Spark connection ID
    application=spark_nonaudit_path,
    jars='/jars/*',
    verbose=False,  # set to True for more verbose output
    dag=dag,
)

spark_nonaudit_task
