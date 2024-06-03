DB_SETTINGS = {
    "DJANGO_db" : dict(
        engine = "postgresql",
        host = "postgres",
        database = "django_db", 
        user = "service",
        password = "service",
        port = 5432
    ),
    "DJANGO_datamart" : dict(
        engine = "postgresql",
        host = "postgres",
        database = "django_datamart", 
        user = "service",
        password = "service",
        port = 5432
    ),
}