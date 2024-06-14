import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import mdates
import seaborn as sns

import psycopg2
from sqlalchemy import create_engine

# PostgreSQL 연결 설정
conn = psycopg2.connect(
    host="postgres",
    database="django_datamart",
    user="service",
    password="service",
    port=5432
)

# 각 테이블에 대한 쿼리 정의
query_access_count = "SELECT * FROM access_count"
query_time_distribution = "SELECT * FROM time_distribution"
query_keyword_check = "SELECT * FROM keyword_check"

# 데이터프레임으로 변환하는 함수 정의
def query_to_dataframe(query, conn):
    cur = conn.cursor()
    cur.execute(query)
    columns = [desc[0] for desc in cur.description]
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=columns)
    cur.close()
    return df

# 각 테이블에 대해 쿼리 실행 및 데이터프레임으로 변환
access_count = query_to_dataframe(query_access_count, conn)
time_distribution = query_to_dataframe(query_time_distribution, conn)
keyword_df = query_to_dataframe(query_keyword_check, conn)

# 연결 종료
conn.close()

# 대시보드 제목
st.markdown('<h1 class="title">CodeGenius BI Dashboard</h1>', unsafe_allow_html=True)
# HTML, CSS 스타일링
st.markdown("""
            <style>
            .title {
                text-align: center;
                color: Blue;
            }
            .header {
                text-align: center;
            }
            .stRadio > div {
                display: flex;
                flex-direction: row;
                justify-content: right;
            }
            .stRadio > label {
                display: none;
            }
            </style>
            """, unsafe_allow_html=True)
# 라디오 버튼 제목
st.markdown('<h2 class="header">Access Count</h2>', unsafe_allow_html=True)
access_count['date'] = pd.to_datetime(access_count['date'])  # date열을 datetime으로 변경
# 체크박스와 버튼을 같은 행에 배치
col1, col2, col3 = st.columns([1, 2, 1])
# 체크박스
with col1:
    show_table1 = st.checkbox("Show table", key='show_table1')
if show_table1:  # 체크박스 선택 시 테이블 표시
    st.dataframe(access_count)
# 버튼
with col3:
    if st.button("Download Data", key='my_button', help="현재 폴더에 'access_count.xlsx'라는 파일명으로 데이터가 저장합니다."):
        access_count.to_excel('access_count.xlsx')
        st.write("데이터가 저장되었습니다.")
# 라디오 버튼
radio_choice1 = st.radio(
    "check",
    ('Homepage', 'History', 'chatting'),
    key='radio_choice1'
)
# 라디오 버튼으로 보여줄 시각화 그래프
if radio_choice1:
    five_days_ago = pd.to_datetime((datetime.now() - timedelta(days=4)).date())
    access_count_filtered = access_count[access_count['date'] >= five_days_ago]
    filtered_df = access_count_filtered[access_count_filtered['html'].str.lower() == radio_choice1.lower()]
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        ax.plot(filtered_df['date'], filtered_df['count'], marker='o')
        ax.set_title(f"{radio_choice1} count over time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Count")
        # 날짜 포맷 지정 및 간격 조정
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        fig.autofmt_xdate()  # 날짜 라벨 자동 회전
        st.pyplot(fig)

# table2 --------------------------------------------------------------------------------------------- 

# 라디오 버튼 제목
st.markdown('<h2 class="header">시간별 이용량 변화</h2>', unsafe_allow_html=True)

# 체크박스와 버튼을 같은 행에 배치
col1, col2, col3 = st.columns([1, 2, 1])

# 체크박스
with col1:
    show_table2 = st.checkbox("Show table", key='show_table2')
if show_table2:  # 체크박스 선택 시 테이블 표시
    st.dataframe(time_distribution)

# 버튼
with col3:
    if st.button("Download Data", key='my_button2', help="현재 폴더에 'time_data.xlsx'라는 파일명으로 데이터가 저장합니다."):
        time_distribution.to_excel('time_data.xlsx')
        st.write("데이터가 저장되었습니다.")

# 시간별 행동 데이터 플롯 함수
def plot_hourly_behavioral_data(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='hour', y='count', marker='o', color='b')
    plt.title('Hourly Behavioral Data Line Plot')
    plt.xlabel('Time')
    plt.ylabel('COUNT')
    st.pyplot(plt.gcf())

# 데이터와 날짜를 사용하여 플롯 생성
batch_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

time_distribution['date'] = pd.to_datetime(time_distribution['date'])
time_distribution = time_distribution[time_distribution['date'] == batch_date]
plot_hourly_behavioral_data(time_distribution)

# table3 ---------------------------------------------------------------------------------------------

# 'component' 열을 하나로 묶음
keyword_df = keyword_df.melt(id_vars=['date'], value_vars=['component_0', 'component_1', 'component_2', 'component_3'],
                     var_name='component_number', value_name='component')

# 'component_number' 열 삭제
keyword_df = keyword_df.drop(columns=['component_number'])

# 라디오 버튼 제목
st.markdown('<h2 class="header">Keyword</h2>', unsafe_allow_html=True)

# 체크박스와 버튼을 같은 행에 배치
col1, col2, col3 = st.columns([1, 2, 1])

# 체크박스
with col1:
    show_table3 = st.checkbox("Show table3", key='show_table3')
if show_table3:  # 체크박스 선택 시 테이블 표시
    st.dataframe(keyword_df)

# 버튼
with col3:
    if st.button("Download Data", key='my_button3', help="현재 폴더에 'keyword_data.xlsx'라는 파일명으로 데이터가 저장합니다."):
        keyword_df.to_excel('keyword_data.xlsx')
        st.write("데이터가 저장되었습니다.")

# 막대 그래프
def plot_bar_chart(df):
    component_counts = df['component'].value_counts()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=component_counts.index, y=component_counts.values)
    plt.title('Component Frequency')
    plt.xlabel('Component')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())


batch_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
keyword_df['date'] = pd.to_datetime(keyword_df['date'])
keyword_df = keyword_df[keyword_df['date'] == batch_date]
plot_bar_chart(keyword_df)