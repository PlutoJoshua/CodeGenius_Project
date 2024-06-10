import pandas as pd

# 데이터 파일 경로
file_path = './raw_data/rawdata.csv'
output_file = './preprocessed_data/preprocessed_rawdata.csv'

# 데이터 읽기
df = pd.read_csv(file_path)

# 결측치 제거
df.dropna(inplace=True)

# 각 컬럼별 특정 키워드 지정
keywords = {
    'label': ["예시", "예제", "url", "\n"],
    'question': ["예시코드", "공식문서", "url", "\n"],
    'answer': ["예시코드", "공식문서", "url", '\n'],
    'code': ["질문", "답", "url"],
    'url': ["질문", "답", "공식문서", "예시", "예제"]
}

# 특정 키워드 제거 함수 지정
def drop_rows_containing_keywords(df, column, keywords):
    for keyword in keywords:
        df = df[~df[column].str.contains(keyword, na=False)]
    return df

# 데이터프레임에서 컬럼별 특정 키워드가 있는 행 제거
for column, keys in keywords.items():
    df = drop_rows_containing_keywords(df, column, keys)
    df.reset_index(drop=True, inplace=True)

# 전처리된 데이터 저장
df.to_csv(output_file, index=False)