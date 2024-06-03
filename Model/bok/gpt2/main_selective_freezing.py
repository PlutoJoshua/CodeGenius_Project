import params  # 파라미터 모듈 임포트
import prepare  # 데이터 준비 모듈 임포트
from transformers import TrainingArguments
from model_loader import ModelLoader
from selective_freezing import SelectiveFreezing
from model_trainer import ModelTrainer

def main():
    model_name = 'skt/kogpt2-base-v2'  # 사용할 모델 이름
    data_path = './data/rawdata.csv'  # 데이터 파일 경로

    # 모델 및 토크나이저 로드
    model_loader = ModelLoader(model_name)
    model, tokenizer = model_loader.load()

    # 데이터 로드 및 준비
    df = prepare.load_data(data_path)
    train_df, test_df = prepare.split_data(df, test_size=0.2)  # 데이터를 학습 및 평가 데이터로 분리
    train_dataset = prepare.prepare_dataset(train_df, tokenizer)  # 학습 데이터셋 준비
    test_dataset = prepare.prepare_dataset(test_df, tokenizer)  # 평가 데이터셋 준비

    # 선택적 프리징
    selective_freezing = SelectiveFreezing(model)
    selective_freezing.freeze_layers([0, 1, 2])

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
    )

    # 모델 학습 및 검증
    trainer = ModelTrainer(model, tokenizer)
    trainer.set_training_args(training_args)  # 학습 인자 설정

    # 모델 학습
    trainer.train(train_dataset, test_dataset)
    trainer.save_model(params.OUTPUT_DIR)

    # 시각화
    trainer.plot_metrics()

if __name__ == "__main__":
    main()
