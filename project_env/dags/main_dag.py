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
    'Code-genius',
    default_args=default_args,
    schedule_interval='@daily'
)

#####################
### etl pipe line ###
#####################

table_name = "test_log"
db_obj = DBconnector(**DB_SETTINGS["DJANGO_log"])
_date = datetime.now() - timedelta(days = 1)
batch_date = _date.strftime("%Y-%m-%d")

def extract_data(db_connector = db_obj, table_name = table_name, batch_date = batch_date):
    with ElapseTime():
        print("extract_data 시작")
        data = extractor(db_connector=db_obj, table_name=table_name, batch_date=batch_date)
    return data

def data_preprocessing(data):
    processed_df = transformer(data)
    return processed_df

# db_obj로 db 변경해야함: setting.py에 추가
table_name = "dmart_log"
db_obj = DBconnector(**DB_SETTINGS["DJANGO_datamart"])

def load_to_pg(df = processed_df, db_connector = db_obj, table_name = table_name):
    with ElapseTime():
        print("load_to_pg 시작")
        loader(df = processed_df, db_connector = db_obj, table_name = table_name)

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