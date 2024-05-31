queries = {
    "test_data" : "SELECT * FROM test_io WHERE created_at::date = '{batch_date}'::date",
    "test_log"  : "SELECT * FROM test_log WHERE insertTime::date = '{batch_date}'::date"
}