import pandas as pd
from db.connector import DBconnector

def extractor(db_connector: DBconnector, table_name: str, batch_date: str) -> pd.DataFrame|list:
    """
    extractor: DBconnector함수에서 가져온 db접속정보와 수정된 쿼리로
    db에서 데이터를 가져와 df로 저장하는 함수
    """
    print("extractor 시작")
    with db_connector as connected:
        try:
            db = connected.postgres_connect
            query = connected.get_query(table_name, batch_date)
            df = pd.read_sql(query, db)
            return df

        except Exception as e:
            print(e)
            return []