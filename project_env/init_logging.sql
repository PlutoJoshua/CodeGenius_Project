CREATE DATABASE django_db;
CREATE DATABASE django_datamart;

-------------------------------------------------------

-- 데이터베이스 연결
\c django_db;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS keyword (
    id SERIAL PRIMARY KEY,
    question TEXT,
    label VARCHAR(3),
    keyword1 VARCHAR(20),
    keyword2 VARCHAR(20),
    keyword3 VARCHAR(20),
    keyword4 VARCHAR(20),
    keyword5 VARCHAR(20)
);

-- Data load
COPY keyword FROM '/docker-entrypoint-initdb.d/keyword.csv' DELIMITER ',' CSV HEADER;

\c django_db;

CREATE TABLE IF NOT EXISTS django_log (
    id SERIAL PRIMARY KEY,
    log_level VARCHAR(10) NOT NULL,
    insertTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    file_name VARCHAR(255) NOT NULL,
    lineno INT NOT NULL,
    log_message TEXT NOT NULL
);
