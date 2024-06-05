queries = {
    "codegenius_access_count" : 
    """
    WITH T1 AS (
        SELECT 
            inserttime,
            substring(log_message FROM '^(.*?)//') AS log_message
        FROM django_log 
        WHERE log_message LIKE '%//%' 
        AND inserttime::date = '{batch_date}'
    )
    SELECT 
        log_message AS html,
        COUNT(log_message) AS access_count,
        inserttime::date as date
    FROM T1
    WHERE inserttime::date = '{batch_date}'
    GROUP BY
        log_message, 
        inserttime::date
    ORDER BY
        log_message ASC
    ;
    """,

    "codegenius_time_distribution" :
    """
    WITH RECURSIVE BASE(N) AS (
        SELECT 0
        
        UNION ALL
        
        SELECT N+1
        FROM BASE 
        WHERE 
            N < 23
        ),
        T1 AS (
        SELECT 
            inserttime,
            substring(log_message FROM '^(.*?)//') AS log_message
        FROM django_log 
        WHERE log_message LIKE '%//%' 
        AND inserttime::date = '{batch_date}'
        ),
        GROUPED_T1 AS (
        SELECT 
            EXTRACT(HOUR FROM inserttime) AS HOUR,
            COUNT(*) AS COUNT,
            inserttime::date AS date
        FROM T1
        GROUP BY EXTRACT(HOUR FROM inserttime), inserttime::date
        )

    SELECT
        BASE.N AS HOUR,
        COALESCE(GROUPED_T1.COUNT, 0) AS COUNT,
        '{batch_date}' AS DATE
    FROM 
        BASE
    LEFT JOIN
        GROUPED_T1
    ON BASE.N = GROUPED_T1.HOUR
    ORDER BY
        BASE.N
    ;
    """,

    "codegenius_keyword" :
    """
    SELECT
        keyword,
        COUNT(keyword) AS keyword_count,
        updated_at::date AS date
    FROM django_io 
    WHERE 
        keyword is not null
        AND updated_at::date = '{batch_date}'
    GROUP BY
        keyword,
        updated_at::date
    ORDER BY
        keyword_count desc,
        keyword asc
    LIMIT 7
    ;
    """,

    "recommendation" :
    """
    SELECT
        user_input
    FROM
        django_io
    WHERE
        classification_label = 'check'
        AND updated_at::date = '{batch_date}'
    ORDER BY
        user_input desc
    ;
    """
}