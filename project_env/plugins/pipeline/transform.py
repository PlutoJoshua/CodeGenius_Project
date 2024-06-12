from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

class TextProcessor_1:
    def __init__(self):
        pass

    def preprocess_text(self, text):
        """
        텍스트 전처리 함수
        """
        text = text.replace(',', ' ')
        return text

    def vectorize_text(self, text_data, max_features=20):
        """
        TF-IDF 벡터화 함수
        """
        vectorizer = TfidfVectorizer(max_features=max_features)
        X = vectorizer.fit_transform(text_data)
        return X, vectorizer

    def reduce_dimensions(self, X, n_components=10, random_state=77):
        """
        차원 축소 함수
        """
        svd = TruncatedSVD(n_components=n_components, random_state=random_state)
        X_reduced = svd.fit_transform(X)
        return X_reduced, svd

    def get_top_keywords(self, model, feature_names, n_top_words):
        """
        주요 키워드 추출 함수
        """
        top_keywords = []
        for topic_idx, topic in enumerate(model.components_):
            top_keywords.append([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        return top_keywords

    def process_text_data(self, text_data, max_features=20, n_components=10, n_top_words=3):
        """
        텍스트 데이터 처리 함수
        """
        # 모든 텍스트 데이터를 결합하여 전처리
        preprocessed_text = ' '.join(text_data.apply(self.preprocess_text))
        
        # 전체 텍스트 데이터에 대해 TF-IDF 벡터화
        X, vectorizer = self.vectorize_text([preprocessed_text], max_features)
        
        # 차원 축소 및 주요 키워드 추출
        X_reduced, svd = self.reduce_dimensions(X, n_components)
        feature_names = vectorizer.get_feature_names_out()
        top_keywords = self.get_top_keywords(svd, feature_names, n_top_words)
        
        return X_reduced, top_keywords
