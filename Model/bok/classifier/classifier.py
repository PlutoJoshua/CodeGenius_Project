import google.generativeai as genai

api_key = "AIzaSyAOBGlVPR_uefBsR01G6HJZ7oQ69-nDGSo"  # 여기에 자신의 API 키를 넣어주세요

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# 프롬프트 엔지니어링
system_prompt =  """
당신은 user_prompt가 파이썬과 관련된 질문인지 아닌지 분류하는 모델입니다.
user_prompt가 파이썬과 관련된 질문 중에서 "파이썬 정의, 파이썬 기초, 조건문, 반복문, 변수, 내장함수, 기본 패키지, 개행문자, 문자열 포맷, tuple, list, set, 넘파이, 판다스, 배열, 행렬, 시각화, matplotlib, seaborn, plotly, 기초통계, 가설검정, 회귀분석, 상관분석, 차이분석, 그룹화, 탐색적 데이터 분석, 데이터 전처리, 데이터의 종류, 데이터의 특성"과 관련된 질문인지 아닌지 분류해주세요.
해당 키워드와 관련된 질문이면 yes로 답변해주세요.
파이썬과 관련된 질문이지만 해당 키워드와 관련이 없는 질문(범위를 벗어난 질문)이라면 check로 답변해주세요.
yes나 no로 분류하기 애매한 질문이라면 check로 답변해주세요.
파이썬과 완전 무관한 질문은 no로 답변해주세요.

답변이 yes인 질문 예시: 문자열의 소문자를 대문자로 변환하는 방법
답변이 no인 질문 예시: 문자열의 소문자를 방법
답변이 check인 질문 예시: 파이썬에서 RNN이 무엇인가요?
"""
# 질문 설정
user_prompt = input()

# 답변 생성
result = model.generate_content(system_prompt + user_prompt)
output = result.text

print(output)