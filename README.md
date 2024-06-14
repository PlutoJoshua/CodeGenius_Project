# CodeGenius
## 천재교육 빅데이터 7기 CodeGenius 팀
<img width="743" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/main1.png">
<br><br>

## ⏩ How to Run
---
> 프로젝트 디렉토리 이동
```sh
cd project_env/
```
> migrate 진행
```sh
docker compose run web python manage.py migrate
```
> docker compose 실행
```sh
docker compose up --build
```
---

## 📥 Postgresql 13 

```sh
cd project_env/
```

```sh
docker exec -it project_env-postgres-1 bash
```

```sh
psql -U service -d {DB}
```

## 🏆Model download link
모델 다운로드 후 CodeGenius_Project/project_env/codegenius/chatbot/service_model/kogpt2_chatbot_model.pth 경로에 지정

```sh
https://drive.google.com/drive/folders/1-7KBtHf8ZT6oPVIB0RduHkw2TK1PUxFz?usp=sharing
```

---

> DB LIST

* DB: django_db             
* DB: django_datamart
--- 
## 🕒 개발 기간
2024.05.21 - 2024.06.13
<br><br>

## 👥 팀원 소개 및 R&R
<img width="743" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/main2.png">
<br><br>

## ℹ 프로젝트 소개
국•내외 챗봇에 대한 관심이 증가함에 따라 코딩 챗봇 교육의 필요성이 부각되었다. 이에 유사한 서비스를 제공하는 챗봇을 분석과 SWOT 분석을 통해 사업전략을 수립하고 챗봇을 개발하였다. 챗봇은 LLM과 프롬프트 엔지니어링을 이용해 개발하였으며, 무료 모델을 사용하여 경제적인 부담을 감소시켰다. </br>
CodeGenius는 실시간 질의 응답이 가능하며, history 창으로 질문한 내용을 저장함과 동시에 행동데이터를 DB에 기록한다. CodeGenius는 기존에 진행하는 교육에 보조 도구로 활용이 가능하며 특히 비전공자에게 적합하다. 대시보드를 활용해 학습자의 행동 데이터를 일마다 관리해 학습 경향 파악이 가능하다. 추후 데이터를 활용한 추가 학습으로 성능을 향상시키고, 더 나아가 유료화를 통해 수익성을 기대할 수 있다. </br>
<br>

## 🛠️ 기능
CodeGenius는 ko-GPT2와 Gemini - OpenAPI를 적용한 챗봇으로, 다양한 기능을 통해 사용자의 학습을 지원한다. 주요 기능은 다음과 같다.</br>
1. 실시간 질의응답</br>
언제 어디서나 가능: 자체 웹 페이지를 통해 언제든지 질문하고 답변을 받을 수 있다.</br>
생성형 언어 모델: 질문자의 의도를 파악하여 파이썬 기초, 통계, Numpy, Pandas에 대한 개념 및 예시 코드를 제공한다.</br>
공식 문서 URL 제공: 주요 라이브러리의 공식 문서 링크를 제공한다.</br>
2. 히스토리 관리</br>
질문 키워드 및 답변 확인: HISTORY 탭에서 날짜별 질문 키워드와 답변을 확인할 수 있다.</br>
주간 인기 키워드: 메인 페이지에서 주간 인기 키워드를 제공한다.</br>
3. 데이터 및 성능 관리</br>
학습행동데이터 수집: 입력 데이터를 저장하여 사용자의 학습 행동 데이터를 수집한다.</br>
성능 향상: 파인 튜닝된 대규모 언어 모델을 통해 추가 학습을 진행하여 성능을 지속적으로 향상시킨다.</br>
대시보드: Airflow를 이용한 대시보드를 통해 학습 경향을 파악할 수 있다.
<br>

## ⚙️ 개발 환경
### ✔️ 사용 언어
<img src="https://img.shields.io/badge/python-3.10.12-E95420?style=for-the-badge&logo=python&logoColor=" style="display:inline;"> <img src="https://img.shields.io/badge/SQL-gray?style=for-the-badge&logo=sql&logoColor=#0078D4" style="display:inline;">

### ✔️ 운영체제 (OS) 및 통합 개발 환경 (IDE)
<img src="https://img.shields.io/badge/Ubuntu-22.04-E95420?style=for-the-badge&logo=Ubuntu&logoColor=#E95420" style="display:inline;"> <img src="https://img.shields.io/badge/windows 11-0078D4?style=for-the-badge&logo=windows11&logoColor=#0078D4" style="display:inline;">  
<img src="https://img.shields.io/badge/googlecolab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white" style="display:inline;"> <img src="https://img.shields.io/badge/visualstudiocode-blue?style=for-the-badge&logo=visualstudiocode&logoColor=white" style="display:inline;"> <img src="https://img.shields.io/badge/docker-darkblue?style=for-the-badge&logo=docker&logoColor=white" style="display:inline;">

### ✔️ 라이브러리
<img src="https://img.shields.io/badge/numpy-1.26.4-EE4C2C?style=for-the-badge&logo=numpy&logoColor=yellow" style="display:inline;"> <img src="https://img.shields.io/badge/pandas-2.2.1-EE4C2C?style=for-the-badge&logo=pandas&logoColor=green" style="display:inline;"> <img src="https://img.shields.io/badge/matplotlib-3.9.0-EE4C2C?style=for-the-badge&logo=matplotlib&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/seaborn-0.13.2-EE4C2C?style=for-the-badge&logo=seaborn&logoColor=#EE4C2C" style="display:inline;">

<img src="https://img.shields.io/badge/pytorch-2.1.2-EE4C2C?style=for-the-badge&logo=Pytorch&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/scikit_learn-1.2.2-EE4C2C?style=for-the-badge&logo=scikit-learn&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/huggingface_hub-0.20.3-EE4C2C?style=for-the-badge&logo=huggingface&logoColor=#EE4C2C" style="display:inline;">

<img src="https://img.shields.io/badge/transformers-4.41.1-EE4C2C?style=for-the-badge&logo=transformers&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/konlpy-0.6.0-EE4C2C?style=for-the-badge&logo=konlpy&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/google_generativeai-0.5.4-EE4C2C?style=for-the-badge&logo=google-generativeai&logoColor=#EE4C2C" style="display:inline;">

<img src="https://img.shields.io/badge/django-5.0-EE4C2C?style=for-the-badge&logo=django&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/redis-5.0.4-EE4C2C?style=for-the-badge&logo=redis&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/django_redis-3.1.3-EE4C2C?style=for-the-badge&logo=django-redis&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/celery-5.4.0-EE4C2C?style=for-the-badge&logo=celery&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/psycopg2_binary-2.9.1-EE4C2C?style=for-the-badge&logo=psycopg2-binary&logoColor=#EE4C2C" style="display:inline;">

<img src="https://img.shields.io/badge/streamlit-1.35.0-EE4C2C?style=for-the-badge&logo=streamlit&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/airflow-2.9.0-EE4C2C?style=for-the-badge&logo=apacheairflow&logoColor=#EE4C2C" style="display:inline;"> <img src="https://img.shields.io/badge/python_dotenv-1.0.1-EE4C2C?style=for-the-badge&logo=dotenv&logoColor=#EE4C2C" style="display:inline;">


## ⚙️ 모델 하이퍼파라미터 튜닝
### ✔️GPT2 모델
`KoGPT2 (skt/kogpt2-base-v2)`
<br/>

## 📝 사용자 매뉴얼
<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual1.png">

<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual2.png">

<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual3.png">

<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual4.png">

<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual5.png">

<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual6.png">

<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual7.png">

<img width="743" height="548" alt="loading..." src="https://github.com/PlutoJoshua/CodeGenius_Project/raw/main/Model/assets/manual8.png">


<br/>

## 🎬 실행 화면 (썸네일 클릭 시 영상 재생)
[![Video Label](http://img.youtube.com/vi/mKGebMXqngw/0.jpg)](https://youtu.be/-qK1lGQBR6I?si=wUpm7huP6amODgWb)

<br/>
