import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

gemini_model = None

def Google_gemini(user_input, api_key):
    global gemini_model
    if gemini_model is None:
        genai.configure(api_key=api_key)
        gemini_model = genai.GenerativeModel('gemini-pro')
        logger.info('classification_model.py/Google_gemini -> gemini model is None, so.... load the gemini model')
    else:
        logger.info('classification_model.py/Google_gemini -> Use cached gemini model')
    
    # 프롬프트 엔지니어링
    system_prompt =  """
    당신은 user_prompt가 파이썬과 관련된 질문인지 아닌지 분류하는 모델입니다.
    user_prompt가 파이썬과 관련된 질문 중에서 "파이썬 기초, 문법, 조건문, 반복문, 연산, 딕셔너리, 예외처리, 객체, 변수, 타입, 함수, 표준 라이브러리, 정규표현식, 문자열, 튜플(tuple), 리스트(list), 해쉬셋(set), 넘파이(numpy), 판다스(pandas), 데이터프레임, 배열, 행렬, 시각화, matplotlib, seaborn, plotly, 통계, 가설 검정, 회귀 분석, 상관 분석, 차이 분석, 분포, 분산 분석, 검증, 가중치, 예측, 시계열 데이터, 등분산성 검정, 통계량, 인코딩, 스케일링, 모델 성능 평가, 람다함수, 행렬, 클러스터링, 오차, 그룹화, 탐색적 데이터 분석, 데이터 전처리, 데이터의 종류, 데이터의 특성"과 관련된 질문인지 아닌지 분류해주세요.
    해당 키워드와 관련된 질문이면 yes로 답변해주세요.
    파이썬과 관련된 질문이지만 해당 키워드의 범위에서 벗어난 질문이라면 check로 답변해주세요.
    yes나 no로 분류하기 애매한 질문이라면 check로 답변해주세요.
    파이썬과 완전 무관한 질문은 no로 답변해주세요.

    답변이 yes인 질문 예시: 문자열의 소문자를 대문자로 변환하는 방법
    답변이 no인 질문 예시: 파이썬 날씨가 어떤가요
    답변이 check인 질문 예시: 파이썬에서 RNN이 무엇인가요
    """

    # 답변 생성
    result = gemini_model.generate_content(system_prompt + user_input)
    output = result.text
    logger.info(f'classification_model.py/Google_gemini -> UserInput: {user_input} classificationOutput: {output}')

    return output