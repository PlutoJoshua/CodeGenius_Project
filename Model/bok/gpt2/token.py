from transformers import GPT2TokenizerFast
import pandas as pd

model_name = 'skt/kogpt2-base-v2'

class CustomTokenizer:
    def __init__(self, base_model_name):
        self.tokenizer = GPT2TokenizerFast.from_pretrained(base_model_name)
    
    # 토큰 초기화 함수
    def initialize_tokens(self, new_vocab):
        self.tokenizer = GPT2TokenizerFast()  # 새로운 토크나이저 생성
        self.tokenizer.add_tokens(new_vocab)
        print("토크나이저가 초기화되었습니다.")
    
    # 새로운 토큰 추가 함수
    def add_new_tokens(self, new_tokens):
        self.tokenizer.add_tokens(new_tokens)
        print("새로운 토큰이 추가된 후 단어 집합 크기:", len(self.tokenizer))
    
    # 토큰 저장 함수
    def save_tokenizer(self, save_path):
        self.tokenizer.save_pretrained(save_path)
        print(f"토크나이저가 {save_path}에 저장되었습니다.")
    
    # 문장 토큰화 함수
    def tokenize_sentence(self, sentence):
        tokens = self.tokenizer(sentence, return_tensors='pt')
        return tokens

# 사용 예시
new_vocab = ["Hello", "world", "I", "am", "a", "new", "tokenizer", 
             "specific", "domain", "specialized", "tokens"]
new_tokens = ["<NEW_TOKEN_1>", "<NEW_TOKEN_2>", "<DOMAIN_SPECIFIC_TOKEN>"]

custom_tokenizer = CustomTokenizer(model_name)
custom_tokenizer.initialize_tokens(new_vocab)
custom_tokenizer.add_new_tokens(new_tokens)
custom_tokenizer.save_tokenizer('./custom_tokenizer')

# 예시 데이터프레임
data = {'sentence': ["Hello, I am testing the new tokenizer.",
                     "This is another example sentence.",
                     "Let's see how this works with multiple sentences."]}
df = pd.DataFrame(data)

# 데이터프레임의 각 문장을 토큰화
df['tokens'] = df['sentence'].apply(lambda x: custom_tokenizer.tokenize_sentence(x))

# 결과 출력
print(df)


"""
# 사용 예시
new_vocab = ["Hello", "world", "I", "am", "a", "new", "tokenizer", 
             "specific", "domain", "specialized", "tokens"]
new_tokens = ["<NEW_TOKEN_1>", "<NEW_TOKEN_2>", "<DOMAIN_SPECIFIC_TOKEN>"]

custom_tokenizer = CustomTokenizer(model_name)
custom_tokenizer.initialize_tokens(new_vocab)
custom_tokenizer.add_new_tokens(new_tokens)
custom_tokenizer.save_tokenizer('./custom_tokenizer')
"""