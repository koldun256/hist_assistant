from dotenv import load_dotenv
import os
from gpt_wrapper import GPTWrapper
from telegram_bot import TelegramBot

load_dotenv()

yc_folder_id = os.getenv("YC_FOLDER_ID")
yc_iam_token = os.getenv("YC_IAM_TOKEN")
telegram_token = os.getenv("TELEGRAM_TOKEN")

gpt = GPTWrapper(yc_folder_id, yc_iam_token)
TelegramBot(telegram_token)
