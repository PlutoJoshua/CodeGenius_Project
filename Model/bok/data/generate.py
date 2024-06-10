import re
import pandas as pd
from prompts import system_prompt, user_prompts

class DataGenerator:
    def __init__(self, model, system_prompt):
        self.model = model
        self.system_prompt = system_prompt
        self.questions = []
        self.answers = []
        self.labels = []
        self.codes = []
        self.urls = []

    def generate_data(self, user_prompt, iterations):
        for _ in range(iterations):
            res = self.model.generate_content(self.system_prompt + user_prompt)
            generated_text = res.text

            # 정규식 패턴 설정 (re.DOTALL 사용)
            pattern = r'질문: (.*?)\n답변: (.*?)\n라벨: (.*?)\n예시코드: (.*?)\n공식문서 URL: (.*?)\n(?=질문:|$)'

            # 각 텍스트에서 질문과 답변을 추출하여 리스트에 저장
            matches = re.findall(pattern, generated_text, re.DOTALL)
            for match in matches:
                self.questions.append(match[0])
                self.answers.append(match[1])
                self.labels.append(match[2])
                self.codes.append(match[3])
                self.urls.append(match[4])

    def to_dataframe(self):
        # 데이터프레임 생성
        df = pd.DataFrame({
            'question': self.questions,
            'answer': self.answers,
            'label': self.labels,
            'code': self.codes,
            'url': self.urls
        })
        return df

    def clear_data(self):
        # 데이터를 초기화하는 메서드
        self.questions = []
        self.answers = []
        self.labels = []
        self.codes = []
        self.urls = []
