from airflow import DAG
from plugins.elastic_search_plugin.hooks.elastic_hook import ElasticHook
from operators.postgres_to_elastic import PostgresToElasticOperator
from airflow.operators.python import PythonOperator
from datetime import datetime



default_args = {
    'start_date': datetime(2020,1,1)
}

def _print_es_info():
    hook = ElasticHook()
    print(hook.info())

with DAG('elasticsearch_dag', schedule_interval='@daily',
        default_args=default_args, catchup=False) as dag:

    print_es_info = PythonOperator(
        task_id = 'print_es_info',
        python_callable = _print_es_info
    )

    connections_to_es = PostgresToElasticOperator(
        task_id='connections_to_es',
        sql='SELECT * FROM connection',
        index='connections'
    )

print_es_info >> connections_to_es