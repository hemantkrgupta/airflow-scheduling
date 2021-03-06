from airflow.models import DAG
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.edgemodifier import Label
from datetime import datetime
import json
from pandas import json_normalize

default_args = {
    'start_date': datetime(2020,1,1)
}

#ti - task instance
def _processing_user(ti):
    users = ti.xcom_pull(task_ids = "extracting_user")
    if not len(users) or 'results' not in users:
        print(len(users))
        print(users)
        raise ValueError("User is empty")
    print(users)
    user = users['results'][0]
    processed_user = json_normalize({
        "firstname": user["name"]["first"],
        "lastname": user["name"]["last"],
        "country": user["location"]["country"],
        "username": user["login"]["username"],
        "password": user["login"]["password"],
        "email": user["email"]
    })
    processed_user.to_csv("/tmp/processed_user.csv", index = None, header = False)

with DAG('user_processing', schedule_interval = '@daily',
    default_args = default_args,
    catchup = False) as dag:
    
    createTable = SqliteOperator(
        task_id = 'creating_table',
        sqlite_conn_id = 'db_sqlite',
        sql = '''
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            )
        '''
    )
    
    isApiAvail = HttpSensor(
        task_id = 'is_api_available',
        http_conn_id = 'user_api',
        endpoint = 'api/'
    )
    
    extractUser = SimpleHttpOperator(
        task_id = 'extracting_user',
        http_conn_id = 'user_api',
        endpoint = 'api/',
        method = 'GET',
        response_filter = lambda response: json.loads(response.text),
        log_response = True
    )
    
    processingUser = PythonOperator(
        task_id = "processing_user",
        python_callable = _processing_user
    )
    
    storingUser = BashOperator(
        task_id = "storing_user",
        bash_command = 'echo -e ".separator ","\n.import /tmp/processed_user.csv users" | sqlite3 /opt/airflow/airflow.db'
    )
    
    createTable >> Label("created") >> isApiAvail >> Label("available") >> extractUser >> Label("extracted") >> processingUser >> Label("processed") >> storingUser
    
    