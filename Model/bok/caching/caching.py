import fasttext
from django.core.cache import cache

# fasttext모델 key
model_key = 'fasttext_model_codegenius'
# 모델 경로 및 파일명(경로: 현재 폴더)
model_path = 'fasttext_model_v1.bin'

# FastText 모델 로드
def load_model(model_path):
    """
    주어진 경로에서 FastText 모델을 로드합니다.
    """
    return fasttext.load_model(model_path)

# FastText 모델 경로를 LocMemCache에 저장하는 함수
def cache_model_path(model_path):
    """
    FastText 모델 경로를 LocMemCache에 저장합니다.
    """
    cache.set(model_key, model_path)  # 모델 경로를 캐시에 저장

# LocMemCache에서 FastText 모델 경로를 가져오는 함수
def get_cached_model_path():
    """
    LocMemCache에서 FastText 모델 경로를 가져옵니다.
    """
    return cache.get(model_key)  # 캐시에서 모델 경로 가져오기 시도