import matplotlib.pyplot as plt
from transformers import Trainer, TrainerCallback, EarlyStoppingCallback
import numpy as np

class ModelTrainer:
    def __init__(self, model, tokenizer):
        """
        모델과 토크나이저를 받아 초기화합니다.
        """
        self.model = model  # 모델 저장
        self.tokenizer = tokenizer  # 토크나이저 저장
        self.trainer = None  # Trainer 초기화
        self.train_args = None  # TrainingArguments 초기화
        self.train_losses = []  # 학습 손실 초기화
        self.eval_losses = []  # 평가 손실 초기화
        self.eval_accuracies = []  # 평가 정확도 초기화

    def set_training_args(self, training_args):
        """
        Trainer를 위한 학습 인자를 설정합니다.
        """
        self.train_args = training_args

    def train(self, train_dataset, eval_dataset):
        """
        주어진 학습 및 평가 데이터셋으로 모델을 학습시킵니다.
        """
        def compute_metrics(eval_pred):
            logits, labels = eval_pred
            predictions = np.argmax(logits, axis=-1)
            accuracy = (predictions == labels).mean()
            return {'accuracy': accuracy}

        self.trainer = Trainer(
            model=self.model,  # 모델 설정
            args=self.train_args,  # 학습 인자 설정
            train_dataset=train_dataset,  # 학습 데이터셋 설정
            eval_dataset=eval_dataset,  # 평가 데이터셋 설정
            compute_metrics=compute_metrics,  # 메트릭 계산 함수 설정
            callbacks=[EarlyStoppingCallback(early_stopping_patience=3), self.LoggingCallback(self)]  # Early Stopping 및 로깅 설정
        )
        
        self.trainer.train()  # 학습 시작

    def save_model(self, save_path):
        """
        학습된 모델을 지정된 경로에 저장합니다.
        """
        self.model.save_pretrained(save_path)  # 모델 저장
        self.tokenizer.save_pretrained(save_path)  # 토크나이저 저장

    def plot_metrics(self, output_file):
        """
        학습과 평가의 정확도 및 손실 변화를 시각화합니다.
        """
        steps = list(range(len(self.train_losses)))  # 스텝 값 생성

        plt.figure(figsize=(10, 5))  # 그래프 크기 설정
        
        # 손실 그래프
        plt.subplot(1, 2, 1)
        plt.plot(steps, self.train_losses, label='Train Loss')  # 학습 손실 그래프
        plt.plot(steps, self.eval_losses, label='Eval Loss')  # 평가 손실 그래프
        plt.xlabel('Steps')  # x축 레이블
        plt.ylabel('Loss')  # y축 레이블
        plt.legend()  # 범례 추가
        plt.title('Training and Evaluation Loss')  # 그래프 제목
        
        # 정확도 그래프
        plt.subplot(1, 2, 2)
        plt.plot(steps, self.eval_accuracies, label='Eval Accuracy')  # 평가 정확도 그래프
        plt.xlabel('Steps')  # x축 레이블
        plt.ylabel('Accuracy')  # y축 레이블
        plt.legend()  # 범례 추가
        plt.title('Training and Evaluation Accuracy')  # 그래프 제목
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close

    class LoggingCallback(TrainerCallback):
        def __init__(self, trainer_instance):
            self.trainer_instance = trainer_instance

        def on_log(self, args, state, control, logs=None, **kwargs):
            if logs is not None:
                if 'loss' in logs:
                    self.trainer_instance.train_losses.append(logs['loss'])
                if 'eval_loss' in logs:
                    self.trainer_instance.eval_losses.append(logs['eval_loss'])
                if 'eval_accuracy' in logs:
                    self.trainer_instance.eval_accuracies.append(logs['eval_accuracy'])
