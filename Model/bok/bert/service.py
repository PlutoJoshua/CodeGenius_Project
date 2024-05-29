import torch
from torch.utils.data import DataLoader, Dataset
import torch.nn as nn
import pandas as pd
from transformers import BertForSequenceClassification
from kobert_tokenizer import KoBERTTokenizer
from tqdm import tqdm

base_model = 'skt/kobert-base-v1'
MODEL_NAME = "./save/model_v1.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 검증할 데이터 정의
class QuestionDataset(Dataset):
    def __init__(self, texts, tokenizer, max_len):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
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
        }
        
# 모델 불러오기
model = BertForSequenceClassification.from_pretrained(base_model, num_labels=2)  # 모델의 아키텍처 설정
model_save_path = MODEL_NAME  # 가중치 불러오기
model.load_state_dict(torch.load(model_save_path))
model = model.to(device)

# 검증 데이터 준비
validation_df = pd.read_excel('./data/valid_set.xlsx')
validation_texts = validation_df['question'].tolist()

max_len = 128
batch_size = 2

tokenizer = KoBERTTokenizer.from_pretrained(base_model)
validation_dataset = QuestionDataset(validation_texts, tokenizer, max_len)
validation_loader = DataLoader(validation_dataset, batch_size=batch_size, shuffle=False)

# 예측 함수 정의
def predict(model, data_loader, device):
    model = model.eval()
    predictions = []

    with torch.no_grad():
        for batch in tqdm(data_loader):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            logits = outputs.logits
            _, preds = torch.max(logits, dim=1)
            predictions.extend(preds.cpu().numpy())

    return predictions

# 예측 수행 및 결과 출력
predictions = predict(model, validation_loader, device)

for text, pred in zip(validation_texts, predictions):
    label = "yes" if pred == 1 else "no"
    print(f"문장: {text} -> 예측된 레이블: {label}")