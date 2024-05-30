import psycopg2
from db import queries
from sqlalchemy import create_engine

class DBconnector:
    def __init__(self, engine: str, host: str, database: str, user: str, password:str, port: str):        
        """
        DBconnector: input은 .env의 정보를 이용한 settings의 DB_SETTINGS
        input data를 conn_params 변수에 넣어 DB에 접속하는 함수
        """
        self.engine = engine

        self.conn_params = dict(
                host = host,
                dbname = database,
                user = user,
                password = password,
                port = port
            )
        self.postgres_connect()
    
        self.sqlalchemy_param = f'{engine}://{user}:{password}@{host}:{port}/{database}'
        self.sqlalchemy_connect()

    def __enter__(self):
        print("enter 접속")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.postgres_connect.close()
        
        print("exit 종료")

    def postgres_connect(self):
        self.postgres_connect = psycopg2.connect(**self.conn_params)

    # db = create_engine(f'{engine_name}://{user_id}:{user_pw}@{host}:{port}/{database}')
    def sqlalchemy_connect(self):
        self.sqlalchemy_connect = create_engine(self.sqlalchemy_param)

    def get_query(self, table_name: str, batch_date: str) -> str:
        _query = postgresql_query.queries[table_name]
        _query = _query.format(batch_date = batch_date)
        return _query