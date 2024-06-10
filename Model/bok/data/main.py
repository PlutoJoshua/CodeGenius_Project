import google.generativeai as genai
from save import save_data

def main():
    # 모델 인스턴스 생성
    api_key = "AIzaSyCLmV2CGmQRyqRlfysRuW1XzOB-2c_Yd44"  # 여기에 자신의 API 키를 넣어주세요
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    # 데이터 생성 및 저장
    save_data(model)

if __name__ == "__main__":
    main()

# 설명
"""
prompts.py에서 프롬프트 엔지니어링을 하여 데이터를 생성합니다.
생성된 데이터는 created_data폴더에 저장됩니다.
main.py를 다시 실행하기전 중복된 데이터가 생기지 않도록 프롬프트를 수정하여 주시고, created_data에 저장된 파일에 번호를 매겨주세요.
파일 번호 예시는 combined_data1.csv, combined_data2.csv, combined_data3.csv ... 이렇게 해주시면 됩니다.
"""