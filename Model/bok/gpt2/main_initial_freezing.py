import params  # 파라미터 모듈 임포트
import prepare  # 데이터 준비 모듈 임포트
from transformers import TrainingArguments
from model_loader import ModelLoader
from initial_freezing import InitialFreezing
from model_trainer import ModelTrainer
import torch

def main():
    model_name = 'skt/kogpt2-base-v2'  # 사용할 모델 이름
    data_path = './data/rawdata.csv'  # 데이터 파일 경로
    output_file = './gpt2_visualization/gpt2_model_v1_metrics.png'  # 그래프 저장 경로

    # GPU 가용성 확인
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("GPU is available. Using GPU:", torch.cuda.get_device_name(0))
    else:
        device = torch.device("cpu")
        print("GPU not available. Using CPU.")

    # 모델 및 토크나이저 로드
    model_loader = ModelLoader(model_name)
    model, tokenizer = model_loader.load()
    model.to(device)  # 모델을 GPU로 이동

    # 데이터 로드 및 준비
    df = prepare.load_data(data_path)
    train_df, test_df = prepare.split_data(df, test_size=0.2)  # 데이터를 학습 및 평가 데이터로 분리
    train_dataset = prepare.prepare_dataset(train_df, tokenizer)  # 학습 데이터셋 준비
    test_dataset = prepare.prepare_dataset(test_df, tokenizer)  # 평가 데이터셋 준비

    # 초기 프리징 및 점진적 언프리징
    initial_freezing = InitialFreezing(model, num_unfreeze_layers=2)
    initial_freezing.apply()

    # 학습 파라미터 설정
    training_args = TrainingArguments(
        output_dir=params.OUTPUT_DIR,  # 모델 출력 디렉토리
        num_train_epochs=params.NUM_TRAIN_EPOCHS,  # 학습 에포크 수
        per_device_train_batch_size=params.BATCH_SIZE,  # 학습 배치 크기
        per_device_eval_batch_size=params.BATCH_SIZE,  # 평가 배치 크기
        learning_rate=params.LEARNING_RATE,  # 학습률
        logging_dir=params.LOGGING_DIR,  # 로깅 디렉토리
        logging_steps=params.LOGGING_STEPS,  # 로깅 빈도
        save_steps=params.SAVE_STEPS,  # 모델 저장 빈도
        evaluation_strategy=params.EVALUATION_STRATEGY,  # 평가 전략
        eval_steps=params.EVAL_STEPS,  # 평가 빈도
        save_total_limit=params.SAVE_TOTAL_LIMIT,  # 저장할 체크포인트의 최대 수
        load_best_model_at_end=True,  # EarlyStoppingCallback를 위한 설정
        # fp16=True,  # 혼합 정밀도 학습(Mixed Precision Training) 활성화 (필요 시)
        # gradient_accumulation_steps=4  # 기울기 누적(Gradient Accumulation) 활성화 (필요 시)
    )

    # 모델 학습 및 검증
    trainer = ModelTrainer(model, tokenizer)
    trainer.set_training_args(training_args)  # 학습 인자 설정

    # 모델 학습
    trainer.train(train_dataset, test_dataset)
    trainer.save_model(params.OUTPUT_DIR)

    # 시각화
    trainer.plot_metrics(output_file)

if __name__ == "__main__":
    main()
