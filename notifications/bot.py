import os
import json
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# 1️⃣ Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, '..')
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
ENV_PATH = os.path.join(ROOT_DIR, '.env')

# 2️⃣ Загружаем .env
load_dotenv(ENV_PATH)

# 3️⃣ Загружаем config.json
if not os.path.isfile(CONFIG_PATH):
    raise FileNotFoundError(f"Файл config.json not founded: {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# 4️⃣ Берём токен и chat_id из .env
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT")

if not TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN or TELEGRAM_CHAT not founded в .env")

config["telegram"]["token"] = TOKEN
config["telegram"]["chat"] = CHAT_ID

# 5️⃣ Подставляем переменные Jenkins, если они есть
JOB_NAME = os.getenv("JOB_NAME", "Unknown Project")
BUILD_URL = os.getenv("BUILD_URL", "")
ENVIRONMENT = os.getenv("ENVIRONMENT", "QA")
COMMENT = os.getenv("COMMENT", "No comment")

config["base"]["project"] = JOB_NAME
config["base"]["reportLink"] = BUILD_URL
config["base"]["environment"] = ENVIRONMENT
config["base"]["comment"] = COMMENT

# 6️⃣ Инициализация бота
bot = Bot(token=TOKEN)

# 7️⃣ Асинхронная отправка сообщения
async def send_message():
    text = (
        f"Project: {config['base'].get('project')}\n"
        f"Finished ✅\n"
        f"Link: {config['base'].get('reportLink')}\n"
        f"Enviroments: {config['base'].get('environment')}\n"
        f"Comment: {config['base'].get('comment')}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=text)
    print("Message sent")

# 8️⃣ Запуск
asyncio.run(send_message())