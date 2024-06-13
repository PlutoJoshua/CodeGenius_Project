import pandas as pd
from db.connector import DBconnector

def loader(df: pd.DataFrame, db_connector: DBconnector, table_name: str) -> bool:
    """
    loader: extractor함수를 통해 db에서 가져온 df를 db에 load하는 함수
    """
    print("loader 시작")
    
    with db_connector as connected:
        try:
            sqlalchemy_conn = connected.sqlalchemy_connect
            
            df.to_sql(
                name = table_name, 
                con = sqlalchemy_conn, 
                if_exists = "replace", 
                index = False
                )
            return True

        except Exception as e:
            print(e)
            return False