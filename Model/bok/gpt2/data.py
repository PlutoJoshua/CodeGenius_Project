import tensorflow as tf
from transformers import AutoTokenizer, TFGPT2LMHeadModel

class Data:
    def __init__(self, train_data, test_data, model_name, batch_size):
        """
        데이터 클래스 초기화
        Args:
        - train_data (pd.DataFrame): 학습 데이터셋
        - test_data (pd.DataFrame): 테스트 데이터셋
        - model_name (str): 사용할 모델의 이름
        - batch_size (int): 배치 크기
        """
        self.train_data = train_data
        self.test_data = test_data
        self.batch_size = batch_size
        # 토크나이저 및 모델 초기화
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, bos_token='<s>', eos_token='</s>', pad_token='<pad>')
        self.model = TFGPT2LMHeadModel.from_pretrained(model_name, from_pt=True)
        # 데이터셋 생성
        self.train_dataset = self.create_train_dataset()
        self.test_dataset = self.create_test_dataset()
        # 데이터셋 길이 계산
        self.train_dataset_length = len(self.train_data) // self.batch_size
        self.test_dataset_length = len(self.test_data) // self.batch_size
    def get_chat_data(self, data):
        """
        데이터에서 질문과 답변을 읽어와 토큰화하여 생성기 형태로 반환
        Args:
        - data (pd.DataFrame): 질문과 답변이 있는 데이터프레임
        Yields:
        - dict: 토큰화된 데이터
        """
        # 데이터에서 질문과 답변을 읽어와 토큰화하여 yield
        for question, answer in zip(data['Q'].to_list(), data['A'].to_list()):
            bos_token = [self.tokenizer.bos_token_id]
            eos_token = [self.tokenizer.eos_token_id]
            sent = self.tokenizer.encode(question + answer)
            yield bos_token + sent + eos_token
    def get_tokenized_data(self, data):
        """
        get_chat_data에서 생성된 데이터를 토큰화된 형태로 생성기 형태로 반환
        Args:
        - data (pd.DataFrame): 질문과 답변이 있는 데이터프레임
        Yields:
        - dict: 토큰화된 데이터
        """
        # get_chat_data에서 생성된 데이터를 토큰화된 형태로 yield
        for encoded in self.get_chat_data(data):
            yield {"input_ids": encoded}
    def create_train_dataset(self):
        """
        학습 데이터셋 생성
        Returns:
        - tf.data.Dataset: 패딩 및 배치가 적용된 학습 데이터셋
        """
        # 학습 데이터셋 생성
        dataset = tf.data.Dataset.from_generator(
            lambda: self.get_tokenized_data(self.train_data),
            output_signature={"input_ids": tf.TensorSpec(shape=[None], dtype=tf.int32)}
        )
        # 패딩 및 배치 적용
        dataset = dataset.padded_batch(
            batch_size=self.batch_size,
            padding_values={"input_ids": self.tokenizer.pad_token_id}
        )
        return dataset.repeat()
    def create_test_dataset(self):
        """
        테스트 데이터셋 생성
        Returns:
        - tf.data.Dataset: 패딩 및 배치가 적용된 테스트 데이터셋
        """
        # 테스트 데이터셋 생성
        def get_questions(data):
            for question in data['Q'].to_list():
                yield self.tokenizer.encode(question)
        dataset = tf.data.Dataset.from_generator(
            lambda: get_questions(self.test_data),
            output_types=tf.int32,
        )
        # 패딩 및 배치 적용
        dataset = dataset.padded_batch(
            batch_size=self.batch_size,
            padded_shapes=[None],
            padding_values=self.tokenizer.pad_token_id
        )
        return dataset.repeat()