import os
import torch
from torch.utils.data import DataLoader, Dataset
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from transformers import BertForSequenceClassification
from kobert_tokenizer import KoBERTTokenizer
from tqdm import tqdm

base_model = 'skt/kobert-base-v1'
MODEL_NAME = "./save/model_v1.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 데이터셋 클래스 정의
class SentimentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]
        encoding = self.tokenizer(
            text,
            max_length=self.max_len,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

# 예제 학습 데이터프레임
df = pd.read_excel('./data/train_set.xlsx')

texts = df['question'].tolist()
df.label = df.label.map({'yes': 1, 'no': 0})
labels = df['label'].tolist()

max_len = 128
batch_size = 2

tokenizer = KoBERTTokenizer.from_pretrained(base_model)
dataset = SentimentDataset(texts, labels, tokenizer, max_len)
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# 모델 로드 및 가중치 초기화
model = BertForSequenceClassification.from_pretrained(base_model, num_labels=2)  # 모델의 아키텍처 설정
model_save_path = MODEL_NAME  # 가중치 불러오기
model.load_state_dict(torch.load(model_save_path))

# 학습 설정
model = model.to(device)

optimizer = optim.AdamW(model.parameters(), lr=5e-5)
loss_fn = nn.CrossEntropyLoss().to(device)

# 학습 함수 정의
def train_epoch(model, data_loader, optimizer, device, n_examples):
    model = model.train()
    losses = 0
    correct_predictions = 0

    for batch in tqdm(data_loader):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        logits = outputs.logits

        _, preds = torch.max(logits, dim=1)
        correct_predictions += torch.sum(preds == labels)
        losses += loss.item()

        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

    return correct_predictions.double() / n_examples, losses / n_examples

# 학습 실행
epochs = 3
for epoch in range(epochs):
    print(f'Epoch {epoch + 1}/{epochs}')
    print('-' * 10)
    train_acc, train_loss = train_epoch(
        model,
        data_loader,
        optimizer,
        device,
        len(dataset)
    )
    print(f'Train loss {train_loss} accuracy {train_acc}')
    
# 모델 저장 경로 설정
def get_model_save_path(base_path, base_filename, ext):
    version = 1
    while True:
        model_save_path = f"{base_path}/{base_filename}_v{version}{ext}"
        if not os.path.exists(model_save_path):
            return model_save_path
        version += 1

# 모델 저장
base_path = './save'
base_filename = 'model'
ext = '.pth'

model_save_path = get_model_save_path(base_path, base_filename, ext)
torch.save(model.state_dict(), model_save_path)
print(f'Model saved to {model_save_path}')