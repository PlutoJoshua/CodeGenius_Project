import logging
import psycopg2
from datetime import datetime

class DatabaseHandler(logging.Handler):
    def __init__(self):
        ### 상속 받은 logging handler 초기화 ###
        super().__init__()
        self.conn = None
        self.connect()        

    def connect(self):
        ### postgresql connect 및 cursor 설정 ###
        self.conn = psycopg2.connect(
            dbname = 'django_db',
            user = 'service',
            password = 'service',
            host = 'postgres',
            port = 5432
        )
        ### auto commit ###
        self.conn.autocommit = True 
        with self.conn.cursor() as cur:
            ### db table 생성(django_log) -> 없을 경우 ###
            create_table_query = '''
                CREATE TABLE IF NOT EXISTS django_log (
                    id SERIAL PRIMARY KEY,
                    log_level VARCHAR(10),
                    insertTime TIMESTAMPTZ,
                    file_name VARCHAR(255),
                    lineno INT,
                    log_message TEXT
                )
            '''
            cur.execute(create_table_query)

    ### Log record를 database에 삽입 ###
    def emit(self, record):
        if self.conn.closed:
            self.connect()

        insert_log_query = '''
            INSERT INTO django_log (log_level, insertTime, file_name, lineno, log_message)
            VALUES (%s, %s, %s, %s, %s)
        '''
        insert_time = datetime.fromtimestamp(record.created).isoformat()
        
        ### with문으로 커서 관리, 커서 닫혔을 경우 다시 연결 ###
        try:
            with self.conn.cursor() as cur:
                cur.execute(insert_log_query, (record.levelname, insert_time, record.pathname, record.lineno, record.msg))
        except (psycopg2.InterfaceError, psycopg2.OperationalError):
            self.connect()
            with self.conn.cursor() as cur:
                cur.execute(insert_log_query, (record.levelname, insert_time, record.pathname, record.lineno, record.msg))
