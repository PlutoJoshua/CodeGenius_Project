import time
import pandas as pd
from generate import DataGenerator
from prompts import system_prompt, user_prompts

def save_data(model):
    # DataGenerator 객체 생성
    data_generator = DataGenerator(model, system_prompt)

    # 모든 데이터를 저장할 데이터프레임 초기화 (컬럼명 설정)
    final_df = pd.DataFrame(columns=['question', 'answer', 'label', 'code', 'url'])
    start = time.time()
    # 각 유저 프롬프트에 대해 데이터 생성 및 저장
    for i, user_prompt in enumerate(user_prompts):
        print(f"프롬프트 {i+1} 시작: {user_prompt}")
        data_generator.generate_data(user_prompt, iterations=10)
        df = data_generator.to_dataframe()
        final_df = pd.concat([final_df, df], ignore_index=True)
        data_generator.clear_data()  # 다음 프롬프트에 대한 데이터를 생성하기 전에 기존 데이터를 초기화
        print(f'프롬프트 {i+1} 완료')
        # # CSV 파일로 저장
        # final_file_name = f'./data/prompt{i+1}_data.csv'
        # df.to_csv(final_file_name, index=False)
        # print(f"프롬프트 {i+1} 완료 및 저장 완료: {final_file_name}")

    # 최종 데이터프레임을 CSV 파일로 저장
    combined_file_name = './created_data/combined_data.csv'
    final_df.to_csv(combined_file_name, index=False)
    end = time.time()
    print(f"모든 프롬프트 완료 및 데이터 결합 완료: {combined_file_name}, 소요시간: {end - start}초")
    
# 설명
"""
prompt별로 반복 생성된 csv파일을 결합하여 하나의 csv파일로 concat하여 저장합니다.
생성된 데이터의 개수는 약 500개 정도이며, 검증이 필요합니다.
main.py파일을 다시 실행하기 위해서는 combined_data1, combined_data2 ... 이런식으로 직접 지정하여야 합니다.
데이터를 다 생성한 후 concat.py를 실행하세요.
"""