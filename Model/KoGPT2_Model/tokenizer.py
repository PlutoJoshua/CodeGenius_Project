from transformers import PreTrainedTokenizerFast # Hugging Face에서 제공하는 토크나이저. 빠르고 효율적인 토크나이징 지원
'''
KoGPT2 모델에서 사용할 토크나이저, 특별 토큰 설정

- MASK : 챗봇 모델이 답변을 생성할 때 정답을 미리 가려놓고 이를 예측하도록 유도하는 용도로 사용
'''
Q_TKN = "<usr>" # 사용자 질문 토큰
A_TKN = "<sys>" # 시스템 응답 토큰
BOS = '</s>' # 시작 토큰
EOS = '</s>' # 종료 토큰
MASK = '<unused0>' # 마스크 토큰 (답변을 가릴 때 사용)
SENT = '<unused1>' # 문장 구분 토큰
PAD = '<pad>' # 패딩 토큰 (시퀀스의 길이를 맞추기 위해 사용)

koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained(
    "skt/kogpt2-base-v2", # KoGPT2 모델의 사전 학습된 가중치를 불러옴
    bos_token=BOS, 
    eos_token=EOS, 
    unk_token='<unk>', # 알 수 없는 토큰 설정
    pad_token=PAD, 
    mask_token=MASK
)

