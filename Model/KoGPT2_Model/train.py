import pandas as pd
from torch.utils.data import DataLoader
from dataset import ChatbotDataset, collate_batch
from model import KoGPT2ChatbotModel
import parameter

def main():
    # 데이터 로드 및 전처리
    Chatbot_Data = pd.read_csv("2024_60_data.csv", index_col=0)
    Chatbot_Data = Chatbot_Data[['question', 'answer']]

    # 데이터셋 및 데이터로더 생성
    train_set = ChatbotDataset(Chatbot_Data)
    train_dataloader = DataLoader(
        train_set, 
        batch_size=parameter.batch_size, 
        shuffle=True, 
        num_workers=parameter.num_workers, 
        collate_fn=collate_batch
    )

    # 모델 초기화 및 학습
    chatbot_model = KoGPT2ChatbotModel(parameter.learning_rate)
    chatbot_model.train(train_dataloader, parameter.epochs)
    chatbot_model.save(parameter.model_save_path)

    # 손실 시각화
    chatbot_model.visualize_losses('./visualization')

if __name__ == "__main__":
    main()