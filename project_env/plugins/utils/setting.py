import os
import dotenv

env_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_path)

DB_SETTINGS = {
    "DJANGO_db" : dict(
        engine = os.environ.get("DATABASE_ENGINE", ""),
        host = os.environ.get("DATABASE_HOST", ""),
        database = os.environ.get("DJANGO_NAME", ""),
        user = os.environ.get("DATABASE_USER", ""),
        password = os.environ.get("DATABASE_PASSWORD", ""),
        port = os.environ.get("DATABASE_PORT", "") 
    ),
    "DJANGO_datamart" : dict(
        engine = os.environ.get("DATABASE_ENGINE", ""),
        host = os.environ.get("DATABASE_HOST", ""),
        database = os.environ.get("DJANGO_DATAMART", ""), 
        user = os.environ.get("DATABASE_USER", ""),
        password = os.environ.get("DATABASE_PASSWORD", ""),
        port = os.environ.get("DATABASE_PORT", "")
    ),
}