from dotenv import load_dotenv
import os

# Выгрузка секретных данных из айда .env. Данный файл должен лежать в данной директории.
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_URL = os.getenv("WEB_URL")
WEB_TOKEN=os.getenv("WEB_TOKEN")
FRONTEND_SERVICE_ID=int(os.getenv("FRONTEND_SERVICE_ID"))

