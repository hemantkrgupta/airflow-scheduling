from airflow.operators.bash import BashOperator
from airflow.models import DAG
from datetime import datetime

with DAG(
    "parallel_dag",
    schedule_interval = "@daily",
    default_args = {"start_date" : datetime(2022,1,1)},
    catchup = False
    ) as dag:
    
    op1 = BashOperator(
        task_id = "task_1",
        bash_command = "sleep 3"
    )
    
    op2 = BashOperator(
        task_id = "task_2",
        bash_command = "sleep 3"
    )
    
    op3 = BashOperator(
        task_id = "task_3",
        bash_command = "sleep 3"
    )
    
    op4 = BashOperator(
        task_id = "task_4",
        bash_command = "sleep 3"
    )
    
    op1 >> [op2, op3] >> op4