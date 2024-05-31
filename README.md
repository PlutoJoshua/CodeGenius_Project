### How to Run
---
> 프로젝트 디렉토리 이동
```sh
cd project_env/
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

* PORT: 8888 -> airflow
* PORT: 8000 -> django

---

### Postgresql 13 

```sh
cd project_env/
```

```sh
docker exec -it project_env-postgres-1 bash
```

```sh
psql -U service -d {DB}
```

---

> DB / TABLE LIST

DB: django_log        
test_log -> 로그 데이터
 
DB: django_db             
keyword -> keyword 추출              
test_io -> data                  