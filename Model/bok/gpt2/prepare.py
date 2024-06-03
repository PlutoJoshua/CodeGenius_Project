import pandas as pd
import torch
from torch.utils.data import Dataset as TorchDataset
from sklearn.model_selection import train_test_split
from datasets import Dataset as HFDataset
from transformers import PreTrainedTokenizer

class TextDataset(TorchDataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item

    def __len__(self):
        return len(self.encodings['input_ids'])

def load_data(file_path: str) -> pd.DataFrame:
    """
    CSV 파일로부터 데이터를 로드하고 question과 answer 컬럼으로 변환합니다.
    """
    df = pd.read_csv(file_path)  # CSV 파일 로드
    df = df[['question', 'answer']]  # 필요한 컬럼만 선택
    return df  # 데이터프레임 반환

def prepare_dataset(df: pd.DataFrame, tokenizer: PreTrainedTokenizer) -> HFDataset:
    """
    데이터프레임을 토크나이저를 사용하여 데이터셋으로 변환합니다.
    """
    questions = df['question'].tolist()  # 질문 리스트로 변환
    answers = df['answer'].tolist()  # 답변 리스트로 변환
    inputs = tokenizer(questions, padding=True, truncation=True, return_tensors='pt')  # 질문 토큰화
    labels = tokenizer(answers, padding=True, truncation=True, return_tensors='pt')  # 답변 토큰화
    
    # inputs['input_ids']와 labels['input_ids']의 길이가 동일한지 확인
    input_lengths = inputs['input_ids'].shape[1]
    label_lengths = labels['input_ids'].shape[1]
    
    # 길이가 다른 경우 최대 길이에 맞춰 토큰화
    if input_lengths != label_lengths:
        max_length = max(input_lengths, label_lengths)
        inputs = tokenizer(questions, padding='max_length', truncation=True, max_length=max_length, return_tensors='pt')
        labels = tokenizer(answers, padding='max_length', truncation=True, max_length=max_length, return_tensors='pt')
    
    dataset = HFDataset.from_dict({
        'input_ids': inputs['input_ids'],  # 입력 토큰 IDs
        'attention_mask': inputs['attention_mask'],  # 어텐션 마스크
        'labels': labels['input_ids']  # 라벨 토큰 IDs
    })
    return dataset  # 데이터셋 반환

def split_data(df: pd.DataFrame, test_size: float=0.2):
    """
    데이터를 학습 및 평가 데이터로 분리합니다.
    """
    train_df, test_df = train_test_split(df, test_size=test_size, random_state=99)  # 데이터 분리
    return train_df.reset_index(drop=True), test_df.reset_index(drop=True)  # 인덱스 리셋 후 반환