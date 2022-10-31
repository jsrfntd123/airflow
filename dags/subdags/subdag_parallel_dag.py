from airflow import DAG
from airflow.operators.bash import BashOperator

def subdag_parallel_subdag(parent_dag_id, child_dag_id, default_args):
    with DAG(dag_id= "{parent}.{child}".format(parent = parent_dag_id, child = child_dag_id),default_args=default_args )as dag:
        extract_a = BashOperator(
            task_id='extract_a',
            bash_command='sleep 1'
        )

        load_a = BashOperator(
            task_id='load_a',
            bash_command='sleep 1'
        )   

        return dag