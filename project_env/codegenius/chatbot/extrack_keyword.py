import logging
from django.db import connection

logger = logging.getLogger(__name__)

def extrack_keyword(user_input):
    try:
        with connection.cursor() as cursor:
            # SQL 쿼리 작성
            _query = """
                SELECT keyword1, keyword2, keyword3, code, code_copy, code_result, url
                FROM (
                    SELECT 
                        keyword1,
                        keyword2,
                        keyword3,
                        keyword4,
                        keyword5,
                        code,
                        code_copy,
                        code_result,
                        url,
                        (CASE WHEN %s LIKE CONCAT('%%', keyword1, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword2, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword3, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword4, '%%') THEN 1 ELSE 0 END +
                         CASE WHEN %s LIKE CONCAT('%%', keyword5, '%%') THEN 1 ELSE 0 END) AS match_count
                    FROM keyword
                ) subquery
                ORDER BY match_count DESC
                LIMIT 1;
            """
            cursor.execute(_query, [user_input, user_input, user_input, user_input, user_input])
            result = cursor.fetchone()
            ### 로깅 ###
            logger.info(f'extract_keyword.py/extrack_keyword -> query done!!, query result: {result}')

            if result:
                keyword1, keyword2, keyword3, code, code_copy, code_result, doc_url = result

                ing = [keyword1, keyword2, keyword3]
                keyword = ''
                for word in ing:
                    if word != "픂뽉쌭":
                        keyword += (" #" + word)

                return {
                    'keyword': keyword,
                    'code': code,
                    'code_copy': code_copy,
                    'code_result': code_result,
                    'doc_url': doc_url
                }

            else:
                logger.error(f'extract_keyword.py/extrack_keyword -> No query results exist')
                return {}

    except Exception as e:
        logger.error(f'extrack_keyword.py/extrack_keyword -> Error: {e}')
        return {}