CREATE DATABASE django_log;
CREATE DATABASE django_db;

\c django_log;

CREATE TABLE IF NOT EXISTS test_log (
    id SERIAL PRIMARY KEY,
    log_level VARCHAR(10) NOT NULL,
    insertTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    filename VARCHAR(255) NOT NULL,
    lineno INT NOT NULL,
    log_message TEXT NOT NULL,
);