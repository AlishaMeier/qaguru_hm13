import os
import json
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT")


with open("config.json", "r") as f:
    config = json.load(f)


config["telegram"]["token"] = TOKEN
config["telegram"]["chat"] = CHAT_ID


bot = Bot(token=config["telegram"]["token"])
bot.send_message(chat_id=config["telegram"]["chat"], text="Finish! ✅")

print("Notification sent to TG")