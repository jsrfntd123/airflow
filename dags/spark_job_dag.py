from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
import os.path
from docker.types import Mount

def checkIfRepoAlreadyCloned():
    if os.path.exists('/home/airflow/simple-app/.git'):
        return 'dummy'
    return 'git_clone'

default_args = {
    'owner'                 : 'airflow',
    'description'           : 'Use of the DockerOperator',
    'depend_on_past'        : False,
    'start_date'            : datetime(2018, 1, 3),
    'email_on_failure'      : False,
    'email_on_retry'        : False,
    'retries'               : 1,
    'retry_delay'           : timedelta(minutes=5)
}

with DAG('spark_job_dag', default_args=default_args, catchup=False) as dag:
    
    t_git_clone = BashOperator(
        task_id='git_clone',
        bash_command='git clone https://github.com/marclamberti/simple-app.git /home/airflow/simple-app'
    )

    # Notice the trigger_rule sets to one_success
    # Why?
    # By default your tasks are set to all_success, so all parents must succeed for the task to be triggered
    # Here t_git_pull depends on either t_git_clone or t_dummy
    # By default if one these tasks is skipped then its downstream tasks will be skipped as well since the trigger_rule is set to all_succeed and so invalidate the task.
    # With one_success, t_git_pull will not be skipped since it now needs only either dummy or git_clone to succeed.
    t_git_pull = BashOperator(
        task_id='git_pull',
        bash_command='cd /home/airflow/simple-app && git pull',
        trigger_rule='one_success'
    )

    t_check_repo = BranchPythonOperator(
        task_id='is_repo_exists',
        python_callable=checkIfRepoAlreadyCloned
    )

    t_dummy = BashOperator(
        task_id="dummy",
        bash_command = 'sleep 1'
    )

    t_docker = DockerOperator(
        task_id='docker_command',
        image='bde2020/spark-master:latest',
        api_version='1.41',
        docker_url='TCP://docker-socket-proxy:2375',
        auto_remove=True,
        environment={
            'PYSPARK_PYTHON': "python3",
            'SPARK_HOME': "/spark"
        },
        mounts=[
            Mount(
                source='/home/airflow/simple-app',
                target='/simple-app',
                type='bind'
            )
        ],
        command='/spark/bin/spark-submit --master local[*] /simple-app/SimpleApp.py',
        network_mode='bridge'
    )

t_check_repo >> t_git_clone
t_check_repo >> t_dummy >> t_git_pull
t_git_clone >> t_git_pull
t_git_pull >> t_docker