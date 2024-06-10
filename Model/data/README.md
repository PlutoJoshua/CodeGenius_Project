# 모델 초기 학습용 데이터를 생성합니다.

## 필독
gemini api key 발급방법: https://aistudio.google.com/app/apikey?hl=ko
.env파일을 생성하여 API_KEY 변수에 발급받은 api key 입력하기

## 반복과정
main.py 실행 >> created_data에 생성된 csv파일에 번호지정 >> prompts.py에서 프롬프트 엔지니어링 >> main.py 실행

## 반복 종료 후 데이터 결합
concat.py 실행

## concat 종료 후 전처리
preprocessing.py 실행
