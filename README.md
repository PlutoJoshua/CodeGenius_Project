### How to Run
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

* DB: django_db             
  * django_io -> data          
  * django_log -> log data                       
  * keyword -> keyword 추출              
  * keyword_top7 -> 전일 keyword 빈도수 탑 7
* DB: django_datamart
  * access_count -> 전일 html 접속 카운트
  * time_distribution -> 전일 시간 별 행동 수
  
