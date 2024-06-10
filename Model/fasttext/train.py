import pandas as pd
import fasttext
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

class FastTextModel:
    def __init__(self, model_path, save_model_path, data_path, epoch=20, lr=0.5, wordNgrams=2, minCount=1, patience=3, output_file=None):
        self.model_path = model_path
        self.save_model_path = save_model_path
        self.data_path = data_path
        self.epoch = epoch
        self.lr = lr
        self.wordNgrams = wordNgrams
        self.minCount = minCount
        self.patience = patience
        self.output_file= output_file
        self.train_accuracies = []
        self.valid_accuracies = []
        self.train_losses = []
        self.valid_losses = []

    # 데이터 불러오기 및 전처리
    def load_and_preprocess_data(self):
        df = pd.read_csv(self.data_path)
        # 라벨 변경
        df['label'] = df['label'].map({'yes': 1, 'no': 0})
        
        # 데이터 분할
        train_df, valid_df = train_test_split(df, test_size=0.2, random_state=42)
        self.train_df = train_df
        self.valid_df = valid_df

    # 질문 포맷팅
    def convert_to_fasttext_format(self, df, filename):
        with open(filename, 'w') as f:
            for _, row in df.iterrows():
                label = f"__label__{row['label']}"
                text = row['question']
                f.write(f"{label} {text}\n")

    # 포맷팅한 데이터 txt파일 형식으로 저장
    def prepare_data(self):
        self.convert_to_fasttext_format(self.train_df, 'train_fasttext.txt')
        self.convert_to_fasttext_format(self.valid_df, 'valid_fasttext.txt')

    # 모델 학습
    def train_model(self, train_file):
        return fasttext.train_supervised(input=train_file, epoch=self.epoch, lr=self.lr, wordNgrams=self.wordNgrams, verbose=2, minCount=self.minCount)

    # 모델 평가 지표
    def evaluate_model(self, model, valid_file):
        result = model.test(valid_file)
        accuracy = result[1]
        loss = result[2]
        return accuracy, loss

    # 모델 학습 및 평가 시작
    def train_and_evaluate(self):
        best_valid_loss = float('inf')
        epochs_no_improve = 0

        for ep in range(1, self.epoch + 1):
            model = self.train_model('train_fasttext.txt')
            
            # 모델 평가
            train_accuracy, train_loss = self.evaluate_model(model, 'train_fasttext.txt')
            valid_accuracy, valid_loss = self.evaluate_model(model, 'valid_fasttext.txt')
            
            self.train_accuracies.append(train_accuracy)
            self.valid_accuracies.append(valid_accuracy)
            self.train_losses.append(train_loss)
            self.valid_losses.append(valid_loss)
            
            print(f"Epoch {ep}/{self.epoch} - Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, Valid Loss: {valid_loss:.4f}, Valid Accuracy: {valid_accuracy:.4f}")
            
            # Early stopping check와 모델 저장을 통합
            if valid_loss < best_valid_loss:
                best_valid_loss = valid_loss
                model.save_model(self.save_model_path)  # Best model 저장
                print(f"Model saved to {self.save_model_path}")
                epochs_no_improve = 0
            else:
                epochs_no_improve += 1
            
            if epochs_no_improve >= self.patience:
                print(f"Early stopping at epoch {ep}")
                break
        
        return self.train_accuracies, self.valid_accuracies, self.train_losses, self.valid_losses

    # 결과 시각화
    def plot_metrics(self):
        epochs = range(1, len(self.train_accuracies) + 1)
        plt.figure(figsize=(12, 5))

        plt.subplot(1, 2, 1)
        plt.plot(epochs, self.train_accuracies, 'bo-', label='Train Accuracy')
        plt.plot(epochs, self.valid_accuracies, 'ro-', label='Valid Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.title('Train and Valid Accuracy')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(epochs, self.train_losses, 'bo-', label='Train Loss')
        plt.plot(epochs, self.valid_losses, 'ro-', label='Valid Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.title('Train and Valid Loss')
        plt.legend()

        plt.tight_layout()
        plt.savefig(self.output_file)
        plt.close()

    # class 내 모든 함수 실행
    def run(self):
        self.load_and_preprocess_data()
        self.prepare_data()
        self.train_and_evaluate()
        self.plot_metrics()
