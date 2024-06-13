from train import FastTextModel

# 필요한 변수 정의
model_path='./saved_model/fasttext_model.bin'  # 학습에 사용될 모델
save_model_path='./saved_model/fasttext_model_v2.bin'  # 학습 후 저상할 모델
data_path='../data/raw_data/rawdata.csv'  # 학습에 사용할 데이터
output_file = './visualization/fasttext_model_v2_metrics.png'  # metrics 시각화 파일
epoch=20
lr=0.5
wordNgrams=2  # 모델이 사용할 단어 n-그램의 최대 길이
minCount=1  # 단어를 포함시키기 위한 최소 빈도 수
patience=3  # Early stop을 위한 설정

if __name__ == "__main__":
    # 모델 학습 및 평가 실행
    model = FastTextModel(
                            model_path=model_path,
                            save_model_path=save_model_path,
                            data_path=data_path,
                            epoch=epoch,
                            lr=lr,
                            wordNgrams=wordNgrams,
                            minCount=minCount,
                            patience=patience,
                            output_file=output_file
                        )
    model.run()