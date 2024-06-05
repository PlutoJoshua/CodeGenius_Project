import torch
import time
import matplotlib.pyplot as plt
import os
import datetime
from transformers import GPT2LMHeadModel

class KoGPT2ChatbotModel:
    def __init__(self, learning_rate=3e-5):
        """
        KoGPT2ChatbotModel 클래스의 초기화 함수입니다.

        Args:
            learning_rate (float): 학습률
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2').to(self.device)
        self.criterion = torch.nn.CrossEntropyLoss(reduction="none")
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        self.Sneg = -1e18 # 마스킹된 위치의 로그 확률을 매우 낮은 값으로 설정 > 그 위치의 토큰이 손실 계산에 기여하지 않도록 함
        self.losses = []  # 손실 값을 기록할 리스트


    def train(self, train_dataloader, epochs):
        """
        모델을 학습시키는 함수입니다.

        Args:
            train_dataloader (DataLoader): 학습 데이터 로더
            epochs (int): 에폭 수
        """
        self.model.train()
        for epoch in range(epochs):
            start_time = time.time()  # 에폭 시작 시간 기록
            epoch_losses = []
            for batch_idx, samples in enumerate(train_dataloader):
                self.optimizer.zero_grad()
                
                
                # 배치를 장치로 이동시킵니다.
                token_ids, mask, label = samples
                token_ids = token_ids.to(self.device)
                mask = mask.to(self.device)
                label = label.to(self.device)
                
                # 순전파를 수행합니다.
                out = self.model(token_ids).logits

                # 마스크를 적용하여 필요한 부분만 학습합니다.
                mask_3d = mask.unsqueeze(dim=2).repeat_interleave(repeats=out.shape[2], dim=2)
                mask_out = torch.where(mask_3d == 1, out, self.Sneg * torch.ones_like(out).to(self.device))
                
                # 손실을 계산합니다.
                loss = self.criterion(mask_out.transpose(2, 1), label)
                
                # 평균 loss 계산
                avg_loss = loss.sum() / mask.sum()

                # 역전파를 수행하여 가중치를 업데이트
                avg_loss.backward()
                self.optimizer.step()

                # 손실 값 기록
                epoch_losses.append(avg_loss.item())

                print(f"Epoch: {epoch+1}/{epochs}, Loss: {avg_loss.item()}")

            # 에폭 손실 값 기록
            self.losses.append(sum(epoch_losses) / len(epoch_losses))

            # 에폭이 끝난 시간 기록 및 출력
            end_time = time.time()
            epoch_time = end_time - start_time
            print(f"Epoch {epoch+1} took {epoch_time:.2f} seconds")

        print("Training complete")

    def save(self, model_save_path):
        """
        모델을 저장하는 함수입니다.

        Args:
            model_save_path (str): 저장 경로
        """
        # 모델 상태 저장
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }, model_save_path)

        print(f"Model saved to {model_save_path}")

    def visualize_losses(self, save_dir):
        """
        학습 손실 값을 시각화하고 저장하는 함수입니다.

        Args:
            save_dir (str): 시각화 이미지를 저장할 디렉토리 경로
        """
        # 시각화 디렉토리를 생성합니다.
        os.makedirs(save_dir, exist_ok=True)

        # 현재 시간을 기반으로 파일 이름을 생성합니다.
        now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        save_path = os.path.join(save_dir, f'loss_plot_{now}.png')

        # 손실 값을 시각화합니다.
        plt.figure(figsize=(10, 5))
        plt.plot(self.losses, label='Training Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training Loss Over Epochs')
        plt.legend()
        plt.savefig(save_path)
        plt.close()
        print(f"Loss plot saved to {save_path}")