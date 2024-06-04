import re
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from parameter import max_len
from tokenizer import koGPT2_TOKENIZER, Q_TKN, A_TKN, SENT, EOS, MASK, PAD

'''
챗봇 모델을 학습하기 위한 데이터셋 클래스와 데이터로더를 정의
PyTorch의 Dataset 및 DataLoader를 사용하여 데이터를 처리하고 모델에 공급하는 역할
'''

class ChatbotDataset(Dataset):
    def __init__(self, chats):
        """
        * ChatbotDataset 초기화 함수

        Args:
            chats (pandas.DataFrame): 질문과 답변이 있는 데이터프레임
            max_len (int): 최대 길이

        Attributes:
            _data (pandas.DataFrame): 질문과 답변 데이터를 담고 있는 데이터프레임
            max_len (int): 최대 길이
            q_token (str): 사용자 발화 토큰
            a_token (str): 시스템 발화 토큰
            sent_token (str): 문장 구분 토큰
            eos (str): 종료 토큰
            mask (str): 마스크 토큰
            tokenizer (transformers.PreTrainedTokenizerFast): 토크나이저
        """
        self._data = chats
        self.max_len = max_len # 모델의 입력을 효율적으로 처리하고 성능을 최적화하기 위한 단계
        self.q_token = Q_TKN
        self.a_token = A_TKN
        self.sent_token = SENT
        self.eos = EOS
        self.mask = MASK
        self.tokenizer = koGPT2_TOKENIZER

    def __len__(self):
        """
        데이터셋의 샘플 수를 반환하는 함수입니다.
        데이터셋의 샘플 수를 반환함으로써 DataLoader가 데이터를 얼마나 묶어서(batch) 가져와야 하는지 결정
        Returns:
            int: 데이터셋의 샘플 수
        """
        return len(self._data)    

    def __getitem__(self, idx):
        """
        주어진 인덱스에 해당하는 데이터셋의 샘플을 반환하는 함수입니다.
        주어진 인덱스를 사용하여 데이터를 토큰화하고, 패딩을 추가하여 모든 샘플이 고정된 길이를 갖도록 처리
        Args:
            idx (int): 인덱스

        Returns:
            tuple: (토큰화된 토큰 ID 리스트, 마스크 리스트, 레이블 ID 리스트)
        """
        # 데이터프레임에서 주어진 인덱스 idx에 해당하는 질문과 답변 데이터를 가져옴
        turn = self._data.iloc[idx]
        q = turn["question"]
        q = re.sub(r"([?!,])", r" ", q) # 구두점 -> 공백 대체
        a = turn["answer"]
        a = re.sub(r"([?!,])", r" ", a) # 구두점 -> 공백 대체

        # 질문, 답변 토크나이즈 / 특수 토큰 추가
        q_toked = self.tokenizer.tokenize(self.q_token + q + self.sent_token)
        q_len = len(q_toked)
        a_toked = self.tokenizer.tokenize(self.a_token + a + self.eos)
        a_len = len(a_toked)

        # 질문의 길이가 최대 길이를 초과할 경우 처리
        if q_len > self.max_len:
            a_len = self.max_len - q_len
            if a_len <= 0:
                q_toked = q_toked[-(int(self.max_len / 2)):] # 질문을 최대 길이의 절반까지 자름
                q_len = len(q_toked)
                a_len = self.max_len - q_len
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)

         # 질문과 답변이 최대 길이를 초과할 경우 처리
        if q_len + a_len > self.max_len:
            a_len = self.max_len - q_len
            if a_len <= 0:
                q_toked = q_toked[-(int(self.max_len / 2)):] # 질문을 최대 길이의 절반까지 자름
                q_len = len(q_toked)
                a_len = self.max_len - q_len
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)

        # 레이블, 마스크 설정
        '''
        레이블: 모델이 예측해야 하는 정답 데이터

        '''
        labels = [self.mask,] * q_len + a_toked[1:] # 질문의 길이만큼 0으로, 답변의 길이만큼 1로 설정
        mask = [0] * q_len + [1] * a_len + [0] * (self.max_len - q_len - a_len) # 마스크 리스트 생성
        labels_ids = self.tokenizer.convert_tokens_to_ids(labels) # 레이블을 토큰 ID로 변환

         # 레이블 ID 리스트가 최대 길이보다 짧을 경우 패딩 추가
        while len(labels_ids) < self.max_len:
            labels_ids += [self.tokenizer.pad_token_id]

        # 토큰 ID 리스트가 최대 길이보다 짧을 경우 패딩 추가
        token_ids = self.tokenizer.convert_tokens_to_ids(q_toked + a_toked)
        while len(token_ids) < self.max_len:
            token_ids += [self.tokenizer.pad_token_id]

        return (token_ids, np.array(mask), labels_ids)

def collate_batch(batch):
    """
    배치 데이터를 처리하는 함수입니다.

    Args:
        batch (list): 배치 데이터

    Returns:
        torch.Tensor: 토큰 ID 텐서
        torch.Tensor: 마스크 텐서
        torch.Tensor: 레이블 ID 텐서
    """
    data = [item[0] for item in batch]
    mask = [item[1] for item in batch]
    label = [item[2] for item in batch]
    return torch.LongTensor(data), torch.LongTensor(mask), torch.LongTensor(label)