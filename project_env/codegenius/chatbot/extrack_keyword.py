import logging
from django.db import connection

logger = logging.getLogger(__name__)

def extrack_keyword(user_input):
    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            _query = """
                SELECT keyword1, keyword2, keyword3, keyword4, 코드, 공식문서url
                FROM (
                    SELECT 
                        idx,
                        keyword1,
                        keyword2,
                        keyword3,
                        keyword4,
                        코드,
                        공식문서url,
                        -- 입력 문자열에 각 키워드가 포함된 횟수를 계산합니다.
                        (CASE WHEN %s LIKE CONCAT('%%', keyword1, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword2, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword3, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword4, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword5, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword6, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword7, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword8, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword9, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword10, '%%') THEN 1 ELSE 0 END) AS match_count
                    FROM keyword_table
                ) subquery
                ORDER BY match_count DESC
                LIMIT 1;
            """
            cursor.execute(_query, [user_input, user_input, user_input, user_input, user_input, user_input, user_input, user_input, user_input, user_input])
            result = cursor.fetchone()
            
            ### 로깅 ###
            logger.info(f'extract_keyword.py/extrack_keyword -> query done!!, query result: {result}')

            if result:
                keyword1, keyword2, keyword3, keyword4, code, doc_url = result
                keyword = '#' + keyword1 + ' #' + keyword2 + ' #' + keyword3 + ' #' + keyword4
                return {
                    'keyword': keyword,
                    'code': code,
                    'doc_url': doc_url
                }
            else:
                logger.error(f'extract_keyword.py/extrack_keyword -> No query results exist')
                return {}

    except Exception as e:
        logger.error(f'extrack_keyword.py/extrack_keyword -> Error: {e}')
        return {}