CREATE DATABASE django_db;
CREATE DATABASE django_datamart;

-----------------------------------------------------------------------------------------------------

-- 데이터베이스 연결
\c django_db;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS keyword (
    id SERIAL PRIMARY KEY,
    keyword1 VARCHAR(50),
    keyword2 VARCHAR(50),
    keyword3 VARCHAR(50),
    keyword4 VARCHAR(50),
    keyword5 VARCHAR(50),
    code TEXT,
    code_copy TEXT,
    code_result TEXT,
    doc_url TEXT
);

-- Data load
COPY keyword FROM '/docker-entrypoint-initdb.d/keyword.csv' DELIMITER ',' CSV HEADER;

-----------------------------------------------------------------------------------------------------

\c django_db;

CREATE TABLE IF NOT EXISTS django_log (
    id SERIAL PRIMARY KEY,
    log_level VARCHAR(10) NOT NULL,
    insertTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    file_name VARCHAR(255) NOT NULL,
    lineno INT NOT NULL,
    log_message TEXT NOT NULL
);

-----------------------------------------------------------------------------------------------------

-- 데이터베이스 선택
\c django_db;

-- 테이블 생성
CREATE TABLE IF NOT EXISTS Label_0_answer (
    id SERIAL PRIMARY KEY,
    answer VARCHAR(255)
);

-- 데이터 로드
COPY Label_0_answer FROM '/docker-entrypoint-initdb.d/Label_0_answer.csv' DELIMITER ',' CSV HEADER;
