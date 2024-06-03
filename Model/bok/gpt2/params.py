# 모델 학습에 사용될 파라미터들을 변수로 저장합니다.

# 경로 설정
OUTPUT_DIR = './results'  # 모델이 저장될 디렉터리
LOGGING_DIR = './logs'  # 로그가 저장될 디렉터리

# 학습 설정
NUM_TRAIN_EPOCHS = 3  # 학습 에포크 수
BATCH_SIZE = 2  # 배치 크기
LEARNING_RATE = 5e-5  # 학습률

# 기타 설정
LOGGING_STEPS = 1000  # 로깅 빈도
SAVE_STEPS = 1000  # 모델 저장 빈도
EVAL_STEPS = 1000  # 평가 빈도
SAVE_TOTAL_LIMIT = 2  # 저장할 체크포인트의 최대 수(가장 최신의 모델 2개만 저장됨)
EVALUATION_STRATEGY = "steps"  # 평가 전략
