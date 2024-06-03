from transformers import GPT2LMHeadModel, GPT2TokenizerFast

class ModelLoader:
    def __init__(self, model_name):
        self.model_name = model_name  # 모델 이름 저장
        self.tokenizer = None  # 토크나이저 초기화
        self.model = None  # 모델 초기화

    def load(self):
        """
        지정된 모델 이름으로부터 GPT-2 모델과 토크나이저를 불러옵니다.
        """
        self.tokenizer = GPT2TokenizerFast.from_pretrained(self.model_name)  # 토크나이저 불러오기
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)  # 모델 불러오기
        
        # 특수 토큰 설정
        special_tokens = {
            'pad_token': '<PAD>',
            'bos_token': '<bos>',
            'eos_token': '<eos>',
            'unk_token': '<unk>',
            'additional_special_tokens': ['<question>', '<answer>']
            }
        
        # 특수 토큰 추가
        self.tokenizer.add_special_tokens(special_tokens)
         
        # 모델의 임베딩 레이어 크기 조정
        self.model.resize_token_embeddings(len(self.tokenizer))
               
        return self.model, self.tokenizer  # 모델과 토크나이저 반환
