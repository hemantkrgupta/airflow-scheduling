from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def demoFunToExecute():
    print("Executed through airflow")

with DAG(
    dag_id = "first_dag",
    schedule_interval = "@daily",
    default_args = {
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 12, 1),
    },
    catchup = False
) as mydag:
    demoFun = PythonOperator(
        task_id = "demoFunToExecute",
        python_callable = demoFunToExecute
    )
