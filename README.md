### How to Run
---
```sh
cd project_env
# migrations 생성
docker compose run web python manage.py makemigrations
# migrate 진행
docker compose run web python manage.py migrate
```
```sh
# docker compose 실행
docker compose up --build
```
---
<br>

* 로컬:8888 -> airflow
* 로컬:8000 -> django