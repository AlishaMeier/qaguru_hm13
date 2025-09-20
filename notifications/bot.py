import os
import json
import asyncio
from dotenv import load_dotenv
from telegram import Bot

# Пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, '..')
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
ENV_PATH = os.path.join(ROOT_DIR, '.env')

# Загружаем .env
load_dotenv(ENV_PATH)

# Загружаем config.json
if not os.path.isfile(CONFIG_PATH):
    raise FileNotFoundError(f"Файл config.json не найден по пути: {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# Получаем токен и чат
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT")

if not TOKEN or not CHAT_ID:
    raise ValueError("TELEGRAM_TOKEN или TELEGRAM_CHAT не найдены в .env")

config["telegram"]["token"] = TOKEN
config["telegram"]["chat"] = CHAT_ID

# Подставляем переменные Jenkins
config["base"]["project"] = os.getenv("JOB_NAME", "Unknown Project")
config["base"]["reportLink"] = os.getenv("BUILD_URL", "")
config["base"]["environment"] = os.getenv("ENVIRONMENT", "QA")
config["base"]["comment"] = os.getenv("COMMENT", "No comment")

# Инициализация бота
bot = Bot(token=TOKEN)

# Асинхронная отправка сообщения
async def send_message():
    text = (
        f"Проект: {config['base'].get('project')}\n"
        f"Сборка завершена ✅\n"
        f"Ссылка: {config['base'].get('reportLink')}\n"
        f"Окружение: {config['base'].get('environment')}\n"
        f"Комментарий: {config['base'].get('comment')}"
    )
    await bot.send_message(chat_id=CHAT_ID, text=text)
    print("Сообщение отправлено в Telegram")

# Запуск
if __name__ == "__main__":
    asyncio.run(send_message())