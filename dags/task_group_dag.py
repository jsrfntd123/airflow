from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from subdags.subdag_parallel_dag import subdag_parallel_subdag
from datetime import datetime
from airflow.utils.task_group import TaskGroup


default_args = {
    'start_date' : datetime(2022, 1, 1)
}
 
with DAG('task_group_dag', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    
    with TaskGroup('processing_tasks') as processing_tasks:
        
        with TaskGroup('spark_task') as spark_task:
            extract_a = BashOperator(
                task_id='extract_a',
                bash_command='sleep 1'
            )

        with TaskGroup('flink_task') as flink_task:
            load_a = BashOperator(
                task_id='load_a',
                bash_command='sleep 1'
            )   
 
    extract_b = BashOperator(
        task_id='extract_b',
        bash_command='sleep 1'
    )
 
    load_b = BashOperator(
        task_id='load_b',
        bash_command='sleep 1'
    )
 
    transform = BashOperator(
        task_id='transform',
        bash_command='sleep 1'
    )
 
    extract_b >> load_b
    [processing_tasks, load_b] >> transform