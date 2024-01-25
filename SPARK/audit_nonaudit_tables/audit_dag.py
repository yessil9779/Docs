from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(datetime.now().year, datetime.now().month, datetime.now().day),
    'email_on_failure': False,
    'email_on_retry': False,
    'catchup': False
}

dag = DAG(
    'audit_dag',
    default_args=default_args,
    description='Audit DAG',
    schedule_interval=timedelta(seconds=15)
)

audit_script_path = '/opt/airflow/dags/spark_scripts/audit_nonaudit_tables/src/audit.py'

audit_task = BashOperator(
    task_id='audit_task',
    bash_command=f'python {audit_script_path}',
    dag=dag,
)

audit_task
