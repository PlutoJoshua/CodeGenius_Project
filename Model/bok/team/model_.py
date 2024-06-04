from transformers import PreTrainedTokenizerFast
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers.optimization import AdamW, get_cosine_schedule_with_warmup
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
import re

Q_TKN = "<usr>"  # 질문 토큰
A_TKN = "<sys>"  # 답변 토큰
BOS = '</s>'  # 문장 시작 토큰
EOS = '</s>'  # 문장 끝 토큰
MASK = '<mask>'  # 마스킹작업 토큰
SENT = '<sent>'  # 문장 구분 토큰
PAD = '<pad>'  # 패딩 토큰
UNK = '<unk>'  # 사전에 없는 토큰

# 모델 및 토큰 불러오기
koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
            bos_token=BOS, eos_token=EOS, unk_token=UNK,
            pad_token=PAD, mask_token=MASK) 
model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')

# 데이터 불러오기
Chatbot_Data = pd.read_csv("rawdata.csv", index_col=0)
Chatbot_Data = Chatbot_Data[['question', 'answer']]

# 챗봇 데이터를 처리하는 클래스를 만든다.
class ChatbotDataset(Dataset):
    def __init__(self, chats, max_len=70):  # 데이터셋의 전처리를 해주는 부분
        self._data = chats
        self.max_len = max_len
        self.q_token = Q_TKN
        self.a_token = A_TKN
        self.sent_token = SENT
        self.eos = EOS
        self.mask = MASK
        self.tokenizer = koGPT2_TOKENIZER

    def __len__(self):  # chatbotdata 의 길이를 리턴한다.
        return len(self._data)

    def __getitem__(self, idx):  # 로드한 챗봇 데이터를 차례차례 DataLoader로 넘겨주는 메서드
        turn = self._data.iloc[idx]
        q = turn["question"]  # 질문을 가져온다.
        q = re.sub(r"([?.!,])", r" ", q)  # 구둣점들을 제거한다.

        a = turn["answer"]  # 답변을 가져온다.
        a = re.sub(r"([?.!,])", r" ", a)  # 구둣점들을 제거한다.

        q_toked = self.tokenizer.tokenize(self.q_token + q + self.sent_token)
        q_len = len(q_toked)

        a_toked = self.tokenizer.tokenize(self.a_token + a + self.eos)
        a_len = len(a_toked)

        #질문의 길이가 최대길이보다 크면
        if q_len > self.max_len:
            a_len = self.max_len - q_len        #답변의 길이를 최대길이 - 질문길이
            if a_len <= 0:       #질문의 길이가 너무 길어 질문만으로 최대 길이를 초과 한다면
                q_toked = q_toked[-(int(self.max_len / 2)) :]   #질문길이를 최대길이의 반으로 
                q_len = len(q_toked)
                a_len = self.max_len - q_len              #답변의 길이를 최대길이 - 질문길이
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)

        #질문의 길이 + 답변의 길이가 최대길이보다 크면
        if q_len + a_len > self.max_len:
            a_len = self.max_len - q_len        #답변의 길이를 최대길이 - 질문길이
            if a_len <= 0:       #질문의 길이가 너무 길어 질문만으로 최대 길이를 초과 한다면
                q_toked = q_toked[-(int(self.max_len / 2)) :]   #질문길이를 최대길이의 반으로 
                q_len = len(q_toked)
                a_len = self.max_len - q_len              #답변의 길이를 최대길이 - 질문길이
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)

        # 답변 labels = [mask, mask, ...., mask, ..., <bos>,..답변.. <eos>, <pad>....]
        labels = [self.mask,] * q_len + a_toked[1:]

        # mask = 질문길이 0 + 답변길이 1 + 나머지 0
        mask = [0] * q_len + [1] * a_len + [0] * (self.max_len - q_len - a_len)
        # 답변 labels을 index 로 만든다.
        labels_ids = self.tokenizer.convert_tokens_to_ids(labels)
        # 최대길이만큼 PADDING
        while len(labels_ids) < self.max_len:
            labels_ids += [self.tokenizer.pad_token_id]

        # 질문 + 답변을 index 로 만든다.    
        token_ids = self.tokenizer.convert_tokens_to_ids(q_toked + a_toked)
        # 최대길이만큼 PADDING
        while len(token_ids) < self.max_len:
            token_ids += [self.tokenizer.pad_token_id]

        #질문+답변, 마스크, 답변
        return (token_ids, np.array(mask), labels_ids)
    
def collate_batch(batch):
    data = [item[0] for item in batch]
    mask = [item[1] for item in batch]
    label = [item[2] for item in batch]
    return torch.LongTensor(data), torch.LongTensor(mask), torch.LongTensor(label)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
train_set = ChatbotDataset(Chatbot_Data, max_len=100)
#윈도우 환경에서 num_workers 는 무조건 0으로 지정, 리눅스에서는 2
train_dataloader = DataLoader(train_set, batch_size=32, num_workers=2, shuffle=True, collate_fn=collate_batch)

model.to(device)
model.train()

learning_rate = 3e-5
criterion = torch.nn.CrossEntropyLoss(reduction="none")
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

epoch = 10
Sneg = -1e18

print("start")
for epoch in range(epoch):
    for batch_idx, samples in enumerate(train_dataloader):
        optimizer.zero_grad()
        
        # 텐서를 적절한 장치로 이동시킵니다.
        token_ids, mask, label = samples
        token_ids = token_ids.to(device)
        mask = mask.to(device)
        label = label.to(device)
        
        # 순전파
        out = model(token_ids)
        out = out.logits  # 로짓 값을 반환하는 새로운 텐서를 얻습니다.
        
        # 추가 작업 수행
        mask_3d = mask.unsqueeze(dim=2).repeat_interleave(repeats=out.shape[2], dim=2)
        mask_out = torch.where(mask_3d == 1, out, Sneg * torch.ones_like(out).to(device))  # Sneg의 장치도 동일하게 설정
        
        loss = criterion(mask_out.transpose(2, 1), label)
        
        # 평균 loss 계산 및 역전파
        avg_loss = loss.sum() / mask.sum()
        avg_loss.backward()
        
        # 학습 끝
        optimizer.step()
        print(f"end{epoch}")
print("end")

# 모델을 저장할 경로를 지정합니다.
model_save_path = 'kogpt2_chatbot_model.pth'

# 모델 상태 저장
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'epoch': epoch,
    'train_loss': avg_loss,
    # 다른 필요한 상태가 있다면 여기에 추가할 수 있습니다.
}, model_save_path)

print(f"Model saved to {model_save_path}")


sent = ""

with torch.no_grad():
    while 1:
        q = input("user > ").strip()
        if q == "quit":
            break
        a = ""
        while 1:
            input_ids = torch.LongTensor(koGPT2_TOKENIZER.encode(Q_TKN + q + SENT + sent + A_TKN + a)).unsqueeze(dim=0).to(device)
            pred = model(input_ids)
            logits = pred.logits
            logits = logits[:, -1, :]  # 마지막 토큰에 대한 로짓
            probs = logits.softmax(dim=-1)
            top_prob, top_idx = torch.topk(probs, k=1, dim=-1)  # 최대 확률과 해당 인덱스
            gen_token_id = top_idx.item()  # 최대 확률을 가진 토큰 인덱스
            gen = koGPT2_TOKENIZER.convert_ids_to_tokens(gen_token_id)
            if gen == EOS:
                break
            a += gen.replace("▁", " ")
        print("Chatbot > {}".format(a.strip()))