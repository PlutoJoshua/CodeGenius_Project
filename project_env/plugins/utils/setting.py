import os
import dotenv

env_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_path)

DB_SETTINGS = {
    "DJANGO_db" : dict(
        engine = os.environ.get("DATABASE_ENGINE", ""),
        host = os.environ.get("DATABASE_HOST", ""), #(호출, 호출value가 없을 경우)
        database = os.environ.get("DJANGO_NAME", ""),
        user = os.environ.get("DATABASE_USER", ""),
        password = os.environ.get("DATABASE_PASSWORD", ""),
        port = os.environ.get("DATABASE_PORT", "") 
    ),
    "DJANGO_log" : dict(
        engine = os.environ.get("DATABASE_ENGINE", ""),
        host = os.environ.get("DATABASE_HOST", ""), #(호출, 호출value가 없을 경우)
        database = os.environ.get("DJANGO_LOG", ""),
        user = os.environ.get("DATABASE_USER", ""),
        password = os.environ.get("DATABASE_PASSWORD", ""),
        port = os.environ.get("DATABASE_PORT", "") 
    ),
}