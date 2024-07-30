import os

from dotenv import load_dotenv

load_dotenv()

# Получение значения DSN
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USERNAME = os.getenv("USERNAME")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_DBNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_DBNAME")
POSTGRES_PORT = os.getenv("POSTGRES_DBNAME")

