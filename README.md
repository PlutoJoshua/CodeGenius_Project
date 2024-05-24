### How to Run
---
> 프로젝트 디렉토리 이동
```sh
cd project_env
```
> migrations 생성
```sh
docker compose run web python manage.py makemigrations
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
<br>

* 로컬:8888 -> airflow
* 로컬:8000 -> django