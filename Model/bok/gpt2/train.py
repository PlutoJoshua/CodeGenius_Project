import tensorflow as tf
from tqdm import tqdm

class ChatbotTrainer:
    def __init__(self, data, learning_rate, optimizer, batch_size, epochs, num_layers_to_freeze):
        """
        챗봇을 훈련하고 평가하는 클래스입니다.
        Args:
            data (Data): 훈련 및 검증 데이터를 관리하는 Data 클래스 객체
            learning_rate (float): 학습률
            optimizer (str): 사용할 옵티마이저 종류. 'adam' 또는 'sgd' 중 하나
            batch_size (int): 배치 크기
            epochs (int): 전체 에폭 수
            num_layers_to_freeze (int): 프리징할 레이어 수
        Attributes:
            data (Data): 훈련 및 검증 데이터를 관리하는 Data 클래스 객체
            batch_size (int): 배치 크기
            epochs (int): 전체 에폭 수
            model (transformers.TFGPT2LMHeadModel): Hugging Face 모델
            optimizer (tf.keras.optimizers.Optimizer): 사용할 옵티마이저
            loss_fn (tf.keras.losses.Loss): 손실 함수
            train_dataset (tf.data.Dataset): 훈련 데이터셋
            test_dataset (tf.data.Dataset): 검증 데이터셋
            train_dataset_length (int): 훈련 데이터셋 길이
            test_dataset_length (int): 검증 데이터셋 길이
            num_layers_to_freeze (int): 프리징할 레이어 수
        """
        self.data = data
        self.batch_size = batch_size
        self.epochs = epochs
        self.model = data.model
        if optimizer.lower() == 'adam':
            self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, epsilon=1e-08)
        elif optimizer.lower() == 'sgd':
            self.optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
        else:
            raise ValueError("Unsupported optimizer type. Please use 'adam' or 'sgd'.")
        self.loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        self.train_dataset = data.train_dataset
        self.test_dataset = data.test_dataset
        self.train_dataset_length = data.train_dataset_length
        self.test_dataset_length = data.test_dataset_length
        self.num_layers_to_freeze = num_layers_to_freeze
        # 프리징 설정
        self.freeze_layers()
        
    def train(self):
        """
        모델을 학습하고 검증하는 메서드
        Returns:
        - tuple: (학습 손실 리스트, 검증 손실 리스트, 검증 정확도 리스트, 에포크 수)
        """
        epoch_losses = []
        epoch_val_losses = []
        epoch_accuracies = []
        
        for epoch in range(self.epochs):
            epoch_loss = 0
            epoch_val_loss = 0
            epoch_accuracy = 0
            # 학습 루프
            for batch in tqdm(self.train_dataset.take(self.train_dataset_length), total=self.train_dataset_length):
                with tf.GradientTape() as tape:
                    # 모델 예측
                    outputs = self.model(batch["input_ids"], training=True)
                    logits = outputs.logits
                    shift_logits = logits[:, :-1, :]
                    shift_labels = batch["input_ids"][:, 1:]
                    mask = tf.cast(shift_labels != self.data.tokenizer.pad_token_id, dtype=tf.float32)
                    # 손실 계산
                    loss = self.loss_fn(shift_labels, shift_logits, sample_weight=mask)
                    batch_loss = tf.reduce_mean(loss)
                # 역전파 및 가중치 업데이트
                gradients = tape.gradient(batch_loss, self.model.trainable_variables)
                self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
                epoch_loss += batch_loss
            epoch_losses.append(epoch_loss / self.train_dataset_length)
            print(f'[Epoch: {epoch + 1:>4}] Training Loss = {epoch_losses[-1]:.4f}')
            # 검증 루프
            for batch in self.test_dataset.take(self.test_dataset_length):
                outputs = self.model(batch, training=False)
                logits = outputs.logits
                shift_logits = logits[:, :-1, :]
                shift_labels = batch[:, 1:]
                mask = tf.cast(shift_labels != self.data.tokenizer.pad_token_id, dtype=tf.float32)
                # 검증 손실 계산
                loss = self.loss_fn(shift_labels, shift_logits, sample_weight=mask)
                epoch_val_loss += tf.reduce_mean(loss)
                # 정확도 계산
                predictions = tf.argmax(shift_logits, axis=-1)
                predictions = tf.pad(predictions, paddings=[[0, 0], [0, tf.shape(shift_labels)[1] - tf.shape(predictions)[1]]], constant_values=self.data.tokenizer.pad_token_id)
                predictions = tf.cast(predictions, dtype=tf.int32)
                shift_labels = tf.cast(shift_labels, dtype=tf.int32)
                accuracy = tf.reduce_sum(tf.cast(tf.equal(predictions, shift_labels), dtype=tf.float32) * mask) / tf.reduce_sum(mask)
                epoch_accuracy += accuracy
            epoch_val_losses.append(epoch_val_loss / self.test_dataset_length)
            epoch_accuracies.append(epoch_accuracy / self.test_dataset_length)
            print(f'[Epoch: {epoch + 1:>4}] Validation Loss = {epoch_val_losses[-1]:.4f}, Accuracy = {epoch_accuracies[-1]:.4f}')
        return epoch_losses, epoch_val_losses, epoch_accuracies, self.epochs
    
    def return_answer_by_chatbot(self, user_text):
        """
        사용자 입력에 대해 챗봇 응답을 반환하는 메서드
        Args:
        - user_text (str): 사용자 입력 텍스트
        Returns:
        - str: 챗봇 응답
        """
        # 입력 텍스트를 토큰화하고 모델에 입력
        sent = '' + user_text + ''
        input_ids = [self.data.tokenizer.bos_token_id] + self.data.tokenizer.encode(sent)
        input_ids = tf.convert_to_tensor([input_ids])
        # 모델 예측 생성
        output = self.model.generate(input_ids, max_length=200, do_sample=True, top_k=20)
        sentence = self.data.tokenizer.decode(output[0].numpy().tolist())
        # 응답에서 토큰 제거
        chatbot_response = sentence.replace('<s>', '').replace('</s>', '')
        return chatbot_response
    
    def freeze_layers(self):
        # 모델의 레이어 수를 얻음
        num_layers = len(self.model.transformer.h)
        # 프리징할 레이어 인덱스 계산
        layers_to_freeze = num_layers - self.num_layers_to_freeze
        # 프리징할 레이어 설정
        for layer in self.model.transformer.h[:layers_to_freeze]:
            layer.trainable = False