import os
import dotenv

env_path = dotenv.find_dotenv()
dotenv.load_dotenv(env_path)

DB_SETTINGS = {
    "POSTGRESQL" : dict(
        engine = os.environ.get("DATABASE_ENGINE", ""),
        host = os.environ.get("DATABASE_HOST", ""), #(호출, 호출value가 없을 경우)
        database = os.environ.get("DATABASE_NAME", ""),
        user = os.environ.get("DATABASE_USER", ""),
        password = os.environ.get("DATABASE_PASSWORD", ""),
        port = os.environ.get("DATABASE_PORT", "") 
    )
}