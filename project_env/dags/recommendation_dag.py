from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pytz

from pipeline.extract import extractor
from pipeline.load import loader
from pipeline.transform import Keyword_transformer

from collections import Counter
import pandas as pd
from db.connector import DBconnector
from db import queries
from utils.setting import DB_SETTINGS
from utils.execution_time_check import ElapseTime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 12, 0, 0, 0, tzinfo=pytz.timezone('Asia/Seoul')),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'recommendation_pipeline',
    default_args=default_args,
    schedule_interval='30 8 * * *',
    catchup=False,
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
    text = df['user_input']
    
    stop_words = ['알려주세요', '알려줘', '파이썬에서', '알고', '싶어', '목적은', '제공하나요', '사용하는', '알려줘요', '위한', '값을', '하나', '사용하여', '다른', '방법은', '방법을', '읽고', '해야', '읽을', '무엇입니까', '쓰는', '써야', '있나', '신경', '뭔가', '무엇인가요', '방법에는', '어떻게', '만드는', '있어', '것이', '하는', '뭐야', '대해', '을', '있나요', '뭔지', '어떤', '의', '방법이', '방법', '흔히']

    ### 인스턴스 ###
    extractor = Keyword_transformer(stop_words=stop_words)
    extractor.transform_data(text)
    
    keywords = extractor.get_keywords(top_n=10)
    processed_df = pd.DataFrame(keywords)

    _date = datetime.now() - timedelta(days=1)
    batch_date = _date.date()
    processed_df['date'] = batch_date
    
    return processed_df

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