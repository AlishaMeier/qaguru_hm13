import os
import json
import asyncio
from dotenv import load_dotenv
from telegram import Bot

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

# Загружаем .env
load_dotenv(os.path.join(BASE_DIR, ".env"))

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT")

if not TOKEN or not CHAT_ID:
    raise ValueError("TOKEN or CHAT_ID not founded. Check .env!")

bot = Bot(token=TOKEN)

async def send_message():
    await bot.send_message(chat_id=CHAT_ID, text="Finish! ✅")
    print("Message sent")

asyncio.run(send_message())