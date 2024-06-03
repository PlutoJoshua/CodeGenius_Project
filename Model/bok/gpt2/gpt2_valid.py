import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

model_path = './results'  # 모델 및 토크나이저가 저장된 디렉터리
num_beams = 5  # 빔 너비: 가능성이 높은 5개의 후보를 유지하고 확장
max_length = 50  # 생성할 텍스트의 최대 길이
num_return_sequences = 1  # 생성할 텍스트의 수
no_repeat_ngram_size = 2  # n-그램 반복 금지 설정: 두 단어 조합 반복 금지

class GPT2ModelValidator:
    def __init__(self, model_path):
        """
        모델과 토크나이저를 로드합니다.
        """
        self.tokenizer = GPT2TokenizerFast.from_pretrained(model_path)  # 토크나이저 로드
        self.model = GPT2LMHeadModel.from_pretrained(model_path)  # 모델 로드
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # GPU가 가용한 경우 GPU 사용
        self.model.to(self.device)  # 모델을 GPU로 이동
        self.model.eval()  # 평가 모드로 전환

    def generate_text(self, input_text, max_length, num_return_sequences, no_repeat_ngram_size, num_beams):
        """
        입력 텍스트에 기반하여 텍스트를 생성합니다.
        """
        # 입력 텍스트를 토크나이저로 토큰화합니다.
        inputs = self.tokenizer(input_text, return_tensors='pt').to(self.device)
        
        # 모델을 사용하여 텍스트를 생성합니다.
        outputs = self.model.generate(
            inputs['input_ids'],
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            no_repeat_ngram_size=no_repeat_ngram_size,
            early_stopping=True,
            num_beams=num_beams
        )
        
        # 생성된 텍스트를 디코딩하여 원래의 텍스트 형식으로 변환: replace 없애면 질문도 같이 출력됨
        generated_texts = [self.tokenizer.decode(output, skip_special_tokens=True).replace(input_text, '') for output in outputs]
        return generated_texts

if __name__ == "__main__":
    validator = GPT2ModelValidator(model_path)
    
    input_text = input()  # 입력 문장
    generated_texts = validator.generate_text(input_text,
                                              max_length,
                                              num_return_sequences,
                                              no_repeat_ngram_size,
                                              num_beams
                                              )

    ## 여러 텍스트 생성 시
    # for i, text in enumerate(generated_texts):
    #     print(f"output {i+1}: {text}")
    
    # 단일 텍스트 생성 시
    print(generated_texts[0])