from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np
import pandas as pd

class Keyword_transformer:
    def __init__(self, n_components=4, n_iter=100, random_state=42, stop_words=None):
        self.n_components = n_components
        self.n_iter = n_iter
        self.random_state = random_state
        self.stop_words = stop_words if stop_words is not None else 'english'
        self.vectorizer = TfidfVectorizer(stop_words=self.stop_words)
        self.svd = TruncatedSVD(n_components=self.n_components, n_iter=self.n_iter, random_state=self.random_state)
        
    def transform_data(self, documents):
        self.documents = documents
        self.X = self.vectorizer.fit_transform(documents)
        self.X_svd = self.svd.fit_transform(self.X)
        self.terms = self.vectorizer.get_feature_names_out()
        
    def get_keywords(self, top_n=10):
        keyword_dict = {}
        for i, comp in enumerate(self.svd.components_):
            terms_comp = zip(self.terms, comp)
            sorted_terms = sorted(terms_comp, key=lambda x: x[1], reverse=True)[:top_n]
            keyword_dict[f"component_{i}"] = [term[0] for term in sorted_terms]
        return keyword_dict