import fasttext

model_path = './fasttext_save/fasttext_model_v1.bin'  # 검증에 사용할 모델 파일 경로
threshold = 0.7  # 임계값

# FastText 모델 로드
def load_model(model_path):
    return fasttext.load_model(model_path)

# FastText를 사용한 라벨 예측 함수 정의
def predict_label(model, text, threshold):
    labels, probabilities = model.predict(text, k=2)  # 두 개의 라벨 확률을 반환하도록 설정
    label_prob_dict = dict(zip(labels, probabilities))
    label_0_prob = label_prob_dict.get('__label__0', 0)
    label_1_prob = label_prob_dict.get('__label__1', 0)
    
    # 임계값에 따라 라벨을 예측하는 로직
    if label_1_prob >= threshold:
        return 1, max(probabilities)
    elif label_0_prob >= threshold and label_0_prob > label_1_prob:
        return 0, max(probabilities)
    else:
        # 두 라벨 모두 임계값 미달인 경우 더 높은 확률을 가진 라벨로 설정
        return (0 if label_0_prob > label_1_prob else 1), max(probabilities)

# 메인 함수
def main(input_text, model_path, threshold):
    # 모델 로드
    model = load_model(model_path)
    
    # 라벨 예측
    predicted_label, probability = predict_label(model, input_text, threshold)
    
    return predicted_label, probability

if __name__ == "__main__":
    input_text = input()  # 입력 문장
    
    label, prob = main(input_text, model_path, threshold)
    print(f"Predicted label: {label}, Probability: {prob}")

# 설명
"""
input을 입력하면 라벨과 분류 정확도를 출력합니다.
"""