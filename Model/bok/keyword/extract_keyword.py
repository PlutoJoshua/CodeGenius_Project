import re
import pandas as pd
import matplotlib.pyplot as plt
from keybert import KeyBERT
from transformers import BertModel
from kiwipiepy import Kiwi
from wordcloud import WordCloud
from sklearn.metrics import precision_score, recall_score

class ExtractKeywords:
    def __init__(self, model_name='skt/kobert-base-v1', stopwords=None, top_n=5):  # stopwords와 top_n 기본값 설정
        self.model_name = model_name
        self.stopwords = stopwords if stopwords else []
        self.top_n = top_n
        self.kiwi = Kiwi()
        self.kw_model = self.load_kw_extractor_model()

    # 키워드 추출 모델 불러오는 함수
    def load_kw_extractor_model(self):
        model = BertModel.from_pretrained(self.model_name)
        kw_model = KeyBERT(model)
        return kw_model

    # 텍스트 전처리 함수
    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        return text

    # 명사 추출 메서드
    def noun_extractor(self, text):
        results = []
        result = self.kiwi.analyze(text)
        for token, pos, _, _ in result[0][0]:
            if len(token) != 1 and (pos.startswith('N') or pos.startswith('SL')):
                results.append(token)
        return results

    # 문장에서 키워드를 추출하는 메서드
    def extract_keywords_from_text(self, text):
        text = self.preprocess_text(text)
        noun = self.noun_extractor(text)
        text_noun = ' '.join(noun)
        keywords = self.kw_model.extract_keywords(text_noun, keyphrase_ngram_range=(1, 1), stop_words=self.stopwords, top_n=self.top_n)
        return [kw[0] for kw in keywords]

    # 데이터 프레임에서 키워드를 추출하는 메서드
    def extract_keywords_from_dataframe(self, dataframe, extract_column_name, label_column_name, label_value):
        max_keywords = 0
        keywords_list = []
        for _, row in dataframe.iterrows():
            # 라벨이 지정된 값과 일치하는 행만 처리
            if row[label_column_name] == label_value:
                text = self.preprocess_text(row[extract_column_name])
                noun = self.noun_extractor(text)
                text_noun = ' '.join(noun)
                keywords = self.kw_model.extract_keywords(text_noun, keyphrase_ngram_range=(1, 1), stop_words=self.stopwords, top_n=self.top_n)
                keyword_texts = [kw[0] for kw in keywords]
                max_keywords = max(max_keywords, len(keyword_texts))
                keywords_list.append(keyword_texts)
            else:
                keywords_list.append([]) 
        
        # 키워드를 데이터프레임에 저장
        for i in range(max_keywords):
            col_name = f'keyword_{i+1}'
            dataframe[col_name] = [keywords[i] if i < len(keywords) else 'N/A' for keywords in keywords_list]
        return dataframe

    # 키워드 시각화 함수
    def visualize_keywords(self, keywords):
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(keywords))
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.show()

    # 성능 평가 함수
    def evaluate_performance(self, true_keywords, pred_keywords):
        true_flat = [item for sublist in true_keywords for item in sublist]
        pred_flat = [item for sublist in pred_keywords for item in sublist]
        precision = precision_score(true_flat, pred_flat, average='micro')
        recall = recall_score(true_flat, pred_flat, average='micro')
        return precision, recall

# 예시 사용법
if __name__ == "__main__":
    # 객체 초기화
    extractor = ExtractKeywords(stopwords=['이', '그', '저'])

    # 텍스트 예제
    text = "오늘 날씨가 정말 좋습니다. 산책을 가고 싶어요."
    keywords = extractor.extract_keywords_from_text(text)
    print("추출된 키워드:", keywords)

    # 데이터프레임 예제
    data = {'text': ["오늘 날씨가 정말 좋습니다.", "산책을 가고 싶어요."], 'label': [0, 1]}
    df = pd.DataFrame(data)
    df_keywords = extractor.extract_keywords_from_dataframe(df, 'text', 'label', 0)
    print("데이터프레임 키워드 추출 결과:")
    print(df_keywords)

    # 키워드 시각화
    extractor.visualize_keywords(keywords)

    # 성능 평가 (예시)
    true_keywords = [['날씨', '정말'], ['산책']]
    pred_keywords = [keywords, []]
    precision, recall = extractor.evaluate_performance(true_keywords, pred_keywords)
    print(f"Precision: {precision}, Recall: {recall}")
