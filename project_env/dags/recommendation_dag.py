from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pytz

from pipeline.extract import extractor
from pipeline.load import loader
from pipeline.transform import TextProcessor_1

import pandas as pd
from db.connector import DBconnector
from db import queries
from utils.setting import DB_SETTINGS
from utils.execution_time_check import ElapseTime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 3, 12, 0, 0, tzinfo=pytz.timezone('Asia/Seoul')),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'recommendation_pipeline',
    default_args=default_args,
    schedule_interval='@daily'
)

def extract_data(**kwargs):
    db_obj = DBconnector(**DB_SETTINGS["DJANGO_db"])
    table_name = "recommendation"
    _date = datetime.now() - timedelta(days=1)
    batch_date = _date.date()
    with ElapseTime():
        print("extract_data 시작")
        return extractor(db_connector=db_obj, table_name=table_name, batch_date=batch_date)

def transform_data(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='fetch_data')

    text_processor = TextProcessor_1()
    X_reduced, top_keywords = text_processor.process_text_data(df['user_input'])

    return df

def load_to_pg(**kwargs):
    db_obj = DBconnector(**DB_SETTINGS["DJANGO_datamart"])
    table_name = "keyword_check"
    processed_df = kwargs['ti'].xcom_pull(task_ids='preprocessing')
    with ElapseTime():
        print("load_to_pg 시작")
        loader(df=processed_df, db_connector=db_obj, table_name=table_name)

with dag:
    fetch_data_task = PythonOperator(
        task_id='fetch_data',
        python_callable=extract_data,
        provide_context=True,
        dag=dag,
    )
    preprocess_task = PythonOperator(
        task_id='preprocessing',
        python_callable=transform_data,
        provide_context=True,
        dag=dag,
    )
    load_to_pg_task = PythonOperator(
        task_id='load_to_pg',
        python_callable=load_to_pg,
        provide_context=True,
        dag=dag,
    )

fetch_data_task >> preprocess_task >> load_to_pg_task