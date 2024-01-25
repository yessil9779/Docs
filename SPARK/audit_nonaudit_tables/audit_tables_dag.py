from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'admin',
    'depends_on_past': False,
    'start_date': datetime(datetime.now().year, datetime.now().month, datetime.now().day),
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'audit_tables_dag',
    default_args=default_args,
    description='Audit Tables DAG',
    schedule_interval=None
)

spark_audit_path = '/opt/airflow/dags/spark_scripts/audit_nonaudit_tables/src/spark_audit.py'

spark_audit_task = SparkSubmitOperator(
    task_id='spark_audit_task',
    conn_id='spark_remote',  # specify your Spark connection ID
    application=spark_audit_path,
    jars='/jars/*',
    verbose=False,  # set to True for more verbose output
    dag=dag,
)

unpause_dag_task = BashOperator(
    task_id='unpause_dag_task',
    bash_command=f'airflow dags unpause audit_dag',
    dag=dag,
)

audit_dag_task = TriggerDagRunOperator(
    task_id='audit_dag_task',
    trigger_dag_id='audit_dag',  
    conf={'key': 'value'}, 
    wait_for_completion=True,
    dag=dag,
)

end_task = DummyOperator(task_id='end_task', dag=dag)

spark_audit_task >> unpause_dag_task >> audit_dag_task >> end_task
