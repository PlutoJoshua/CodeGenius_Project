from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from pipeline.extract import extractor
from pipeline.transform import transformer
from pipeline.load import loader

from db.connector import DBconnector
from db import queries
from utils.setting import DB_SETTINGS
from utils.execution_time_check import ElapseTime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2099, 1, 1),
    'retries': 1
}

dag = DAG(
    'Django_Log',
    default_args=default_args,
    schedule_interval='@daily'
)

#####################
### etl pipe line ###
#####################

def extract_data():
    data = extractor()
    return data

def data_preprocessing(data):
    processed_df = transformer(data)
    return processed_df

def load_to_pg(processed_df):
    loader(processed_df)

############
### task ###
############

with dag:
    extract_data_task = PythonOperator(
        task_id='Extract_Log',
        python_callable=extract_data,
    )
    data_preprocessing_task = PythonOperator(
        task_id='Data_processing',
        python_callable=data_preprocessing,
        op_args = [extract_data_task.output]
    )
    load_to_mysql_task = PythonOperator(
        task_id='Load_to_postgresql',
        python_callable=load_to_pg,
        op_args = [data_preprocessing_task.output]
    )

#######################
### task dependency ###   
#######################

extract_data_task >> data_preprocessing_task >> load_to_mysql_task