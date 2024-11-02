import os

DB_PASSWORD = os.getenv("mysql_root_pwd")

FUELO_API_KEY = os.getenv("FUELO_API_KEY")

API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")