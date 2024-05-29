import pandas as pd
import fasttext
import matplotlib.pyplot as plt

# 변수 지정
model_path = './fasttext_save/fasttext_model_v1.bin'
epoch = 20  # 최대 epoch 수
lr = 0.5
wordNgrams = 2
minCount = 1
patience = 3  # Early stopping patience

# 데이터 로드 및 전처리
train_df = pd.read_excel('./data/train_set.xlsx')
valid_df = pd.read_excel('./data/valid_label_set.xlsx')

# 라벨 변환
train_df.label = train_df.label.map({'yes': 1, 'no': 0})
valid_df.label = valid_df.label.map({'yes': 1, 'no': 0})

# FastText 형식으로 변환
def convert_to_fasttext_format(df, filename):
    with open(filename, 'w') as f:
        for _, row in df.iterrows():
            label = f"__label__{row['label']}"
            text = row['question']
            f.write(f"{label} {text}\n")

convert_to_fasttext_format(train_df, 'train_fasttext.txt')
convert_to_fasttext_format(valid_df, 'valid_fasttext.txt')

# 모델 학습 및 평가 기록 저장
def train_and_evaluate(train_file, valid_file):
    train_accuracies = []
    valid_accuracies = []
    train_losses = []
    valid_losses = []
    model = None  # 모델 변수를 함수 밖에서도 사용할 수 있도록 설정
    
    best_valid_loss = float('inf')
    epochs_no_improve = 0
    
    for ep in range(1, epoch + 1):
        model = fasttext.train_supervised(input=train_file, epoch=ep, lr=lr, wordNgrams=wordNgrams, verbose=2, minCount=minCount)
        
        # Train set evaluation
        train_result = model.test(train_file)
        train_accuracy = train_result[1]
        train_loss = train_result[2]

        # Valid set evaluation
        valid_result = model.test(valid_file)
        valid_accuracy = valid_result[1]
        valid_loss = valid_result[2]
        
        train_accuracies.append(train_accuracy)
        valid_accuracies.append(valid_accuracy)
        train_losses.append(train_loss)
        valid_losses.append(valid_loss)

        print(f"Epoch {ep}/{epoch} - Train Loss: {train_loss:.4f}, Train Accuracy: {train_accuracy:.4f}, Valid Loss: {valid_loss:.4f}, Valid Accuracy: {valid_accuracy:.4f}")

        # Early stopping check
        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            epochs_no_improve = 0
            model.save_model(model_path)  # Best model 저장
            print(f"Model saved to {model_path}")
        else:
            epochs_no_improve += 1
        
        if epochs_no_improve >= patience:
            print(f"Early stopping at epoch {ep}")
            break

    return train_accuracies, valid_accuracies, train_losses, valid_losses

# 모델 평가항목
train_accuracies, valid_accuracies, train_losses, valid_losses = train_and_evaluate('train_fasttext.txt', 'valid_fasttext.txt')

print("Train accuracy", train_accuracies)
print("Valid accuracy", valid_accuracies)
print("Train loss", train_losses)
print("Valid loss", valid_losses)