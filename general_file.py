import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение значения DSN
DATABASE_URL = os.getenv("DATABASE_URL")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
USERNAME = os.getenv("USERNAME")




