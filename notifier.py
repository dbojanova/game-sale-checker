import requests
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_notification(message):
	url=f"https://api.telegram.org/bot{TOKEN}/sendMessage"
	post_data={
		"chat_id":CHAT_ID,
		"text":message
	}
	requests.post(url,data=post_data)