import os
import pandas as pd

temp = pd.DataFrame(columns=['question', 'answer', 'label', 'code', 'url'])
csvs = os.listdir('combined_data')

for i in range(1, len(csvs)+1):
    df = pd.read_csv(f'created_data/combined_data{i}.csv')
    df = df.fillna("없음")  # 결측치 처리
    temp = pd.concat([temp,df], ignore_index=True)

temp.to_csv('./raw_data/rawdata.csv', index=False)

# 설명
"""
combined_data 디렉터리에 있는 csv파일을 모두 읽어와서 concat하여 raw_data 폴더에 저장합니다.
"""