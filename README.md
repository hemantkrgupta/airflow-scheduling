# airflow-scheduling
This repository contains different airflow dags to demonstrate working with airflow.

## Run airflow on Gitpod using Docker
In this project, we will be running airflow on Gitpod using Docker. An easy to follow procedure is already available on the official website of docker, which shows how to run airflow using Docker. Link is present in references. Otherwise, following commands can be used to start airflow:
1. `curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.2.3/docker-compose.yaml'`
2. `mkdir -p ./dags ./logs ./plugins`
3. `echo -e "AIRFLOW_UID=$(id -u)" > .env`
4. `docker-compose up airflow-init`
5. `docker-compose up`

After this, hopefully your airflow would be up and running. You can go to airflow UI and enter username and password as airflow. Here you will be able to see all the example dags.

We have a user processing dag, in which we have five tasks. Following are the tasks:
1. Create table to store user data
2. Check if API is available from which data will be extracted.
3. Extract the user data.
4. Process user data.
5. Store user data.

In the user_processing dag, a DB and an HTTP connection is being used. First we will create the database to use and then we will create these connections. 
## Create Database
To create a database, go to worker container using
`docker exec -it <container name> /bin/bash` and create a db in home path using `sqlite3 airflow.db`. This will create an sqllite database which we will be using to store user data.

## Create Airflow DB Connection
1. Go to airflow UI -> admin -> connection -> add a new record
2. Enter connection id - db_sqlite
3. Enter connection type - sqlite
4. Enter description - SQLITE connection to DB
5. Enter host - /opt/airflow/airflow.db
6. Enter login - airflow
7. Enter password - airflow
8. Save this connection, it will be used in data pipeline

## Create an HTTP Connection
1. connection id - user_api
2. connection type - https
3. description - API for getting users
4. host - https://randomuser.me/

After setting up it all, try running this dag from airflow UI.

## References
https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html
