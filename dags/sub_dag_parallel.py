from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
from subdags.subdag_parallel_dag import subdag_parallel_subdag
from datetime import datetime


default_args = {
    'start_date' : datetime(2022, 1, 1)
}
 
with DAG('subdag_parallel', default_args=default_args, schedule_interval='@daily', catchup=False) as dag:

    #Define the subdags creating a function wich return the DAG. You have to provide the same default args that original DAG
    #Subdags ere not recommended because these can cause dead loks and in subdags you only can execute the sequential executor type.
    processing = SubDagOperator(
        task_id='processing_tasks',
        subdag= subdag_parallel_subdag('subdag_parallel','processing_tasks',default_args)
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
    [processing, load_b] >> transform