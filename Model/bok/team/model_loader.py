from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel

# 불러올 모델
model_name = "skt/kogpt2-base-v2"

# 추가할 토큰들
BOS = '</s>'  # 문장 시작 토큰
EOS = '</s>'  # 문장 끝 토큰
UNK = '<unk>'  # 사전에 없는 토큰
PAD = '<pad>'  # 패딩 토큰
MASK = '<mask>'  # 마스킹작업 토큰
# prepare에 사용될 토큰들
Q_TKN = "<usr>"  # 질문 토큰
A_TKN = "<sys>"  # 답변 토큰
SENT = '<sent>'  # 문장 구분 토큰

class ModelLoader:
    def __init__(self, model_name):
        self.model_name = model_name
        self.bos = BOS
        self.eos = EOS
        

    def model_loader(self):
        # 모델 및 토큰 불러오기
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(self.model_name,
                    bos_token=BOS, eos_token=EOS, unk_token=UNK,
                    pad_token=PAD, mask_token=MASK) 
        return self.model, self.tokenizer