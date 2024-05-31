# 모델
 - 모델 실행 환경: WSL Ubuntu22.04

## 모델 학습 방법 및 결과
1. fasttext모델
- 방법: fasttext 디렉터리 경로로 이동 후 python3 main.py
- 결과: fasttext_save 디렉터리에 학습된 모델 저장, 그래프

## 모델 디렉터리 구조
```
├── data
│   ├── create
│   │   ├── concat_data.ipynb
│   │   ├── data_generate.ipynb
│   │   ├── enddata
│   │   ├── rawdata
│   │   └── testdata
│   │       ├── data1_1
│   │       ├── data1_2
│   │       ├── data1_3
│   │       ├── data2_1
│   │       ├── data2_2
│   │       ├── data2_3
│   │       └── data2_4
│   ├── test
│   ├── train
│   └── valid
├── fasttext
│   ├── fasttext_save
│   │   ├── fasttext_model.bin
│   │   ├── fasttext_model_v1.bin
│   │   └── fasttext_model_v2.bin
│   ├── fasttext_train.py
│   ├── fasttext_valid.py
│   ├── fasttext_visualization
│   ├── main.py
│   ├── requirements.txt
│   ├── train_fasttext.txt
│   └── valid_fasttext.txt
├── gpt2
│   ├── data.py
│   ├── gpt2_chatbot
│   │   ├── added_tokens.json
│   │   ├── config.json
│   │   ├── generation_config.json
│   │   ├── merges.txt
│   │   ├── special_tokens_map.json
│   │   ├── tf_model.h5
│   │   ├── tokenizer.json
│   │   ├── tokenizer_config.json
│   │   └── vocab.json
│   ├── model.ipynb
│   ├── model_test.ipynb
│   ├── requirements.txt
│   ├── service.py
│   └── train.py
└── keyword
    ├── keyword.csv
    ├── keyword.ipynb
    ├── keyword.py
    ├── requirements.txt
    └── stopwords.txt
```