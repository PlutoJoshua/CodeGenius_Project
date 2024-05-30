import fasttext
from django.core.cache import caches
import logging

logger = logging.getLogger(__name__)

### Django Redis 캐시 ###
redis_cache = caches['default']

### 모델 변수 ###
fasttext_model = None

### 글로벌 변수로 FastText 모델 로드 후 저장 ###
def load_model(model_path):
    global fasttext_model
    if fasttext_model is None:
        fasttext_model = fasttext.load_model(model_path)
         ### 모델 경로를 캐시에 저장 ###
        redis_cache.set('fasttext_model_path', model_path) 
    return fasttext_model

### FastText를 사용한 라벨 예측 함수 정의 ###
def predict_label(model, text, threshold):
    if model is None:
        logger.error("classification_model.py/predict_label -> predict_label -> model is None!!!")
        return None
    
    ### 두 개의 라벨 확률을 반환하도록 설정 ###
    labels, probabilities = model.predict(text, k=2)  
    label_prob_dict = dict(zip(labels, probabilities))
    label_0_prob = label_prob_dict.get('__label__0', 0)
    label_1_prob = label_prob_dict.get('__label__1', 0)
    
    ### 임계값에 따라 라벨을 예측하는 로직 ###
    if label_1_prob >= threshold:
        return 1, max(probabilities)
    elif label_0_prob >= threshold and label_0_prob > label_1_prob:
        return 0, max(probabilities)
    else:
        ### 두 라벨 모두 임계값 미달인 경우 더 높은 확률을 가진 라벨로 설정 ###
        return (0 if label_0_prob > label_1_prob else 1), max(probabilities)

### 실행 함수 ###
def main(input_text, model_path, threshold):
    ### 모델 로드 ###
    model = load_model(model_path)
    if model is None:
        logger.error("classification_model.py/main -> Model loading failed, unable to proceed.")
        return None
    
    # 라벨 예측
    predicted_label, probability = predict_label(model, input_text, threshold)
    logger.info(f'classification output: {predicted_label}, probability: {probability}')
    return predicted_label