from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pytz
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from konlpy.tag import Okt

okt = Okt()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 3, 8, 0, 0, tzinfo=pytz.timezone('Asia/Seoul')),
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
        extracted_data = extractor(db_connector=db_obj, table_name=table_name, batch_date=batch_date)
        kwargs['ti'].xcom_push(key='extracted_data', value=extracted_data)

def preprocess_and_train(**kwargs):
    ti = kwargs['ti']
    df = ti.xcom_pull(key='extracted_data', task_ids='fetch_data')
    
    def preprocess_text(text):
        tokens = okt.nouns(text)
        return ' '.join(tokens)
    
    df['processed'] = df['user_input'].apply(preprocess_text)

    # TF-IDF 및 LDA 학습
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['processed'])
    
    lda = LatentDirichletAllocation(n_components = 4, random_state = 777)
    lda.fit(tfidf_matrix)
    
    df['lda_topic'] = lda.transform(tfidf_matrix).argmax(axis=1)
    kwargs['ti'].xcom_push(key='processed_data', value=df)

def load_to_pg(**kwargs):
    db_obj = DBconnector(**DB_SETTINGS["DJANGO_datamart"])
    table_name = "lda_userInput"
    processed_df = kwargs['ti'].xcom_pull(task_ids='preprocess_and_train', key='processed_data')
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
    preprocess_and_train_task = PythonOperator(
        task_id='preprocess_and_train',
        python_callable=preprocess_and_train,
        provide_context=True,
        dag=dag,
    )
    load_to_pg_task = PythonOperator(
        task_id='load_to_pg',
        python_callable=load_to_pg,
        provide_context=True,
        dag=dag,
    )

fetch_data_task >> preprocess_and_train_task >> load_to_pg_task