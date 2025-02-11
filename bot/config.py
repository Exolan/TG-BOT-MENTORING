import os
from dotenv import load_dotenv

#Загружаем переменные из .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=int(os.getenv("DB_PORT"))
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR")
IMAGES_DIR = os.getenv("IMAGES_DIR")