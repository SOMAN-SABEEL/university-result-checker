import requests
from bs4 import BeautifulSoup
import os

URL = "https://egov.uok.edu.in/results/"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

KEYWORDS = [
    "b. tech 1st semester regular batch 2025 and backlog batches"
]

def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(telegram_url, data=data)

    if response.status_code == 200:
        print("Telegram notification sent")
    else:
        print("Telegram notification failed")

try:
    response = requests.get(URL, timeout=20)

    if response.status_code != 200:
        print(f"Website error: {response.status_code}")
        exit()

    soup = BeautifulSoup(response.text, "html.parser")

    page_text = soup.get_text().lower()

    found_keywords = []

    for keyword in KEYWORDS:
        if keyword.lower() in page_text:
            found_keywords.append(keyword)

    if found_keywords:
        message = (
            "1st Semester Result Notification May Be Out\n\n"
            "Detected Keywords:\n- "
            + "\n- ".join(found_keywords)
        )

        print(message)

        send_telegram_message(message)

    else:
        print("No result notification found yet.")

except Exception as e:
    print(f"Error: {e}")