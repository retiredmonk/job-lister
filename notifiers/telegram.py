from .utility import send_with_retry
from config import TELEGRAM_URL, TELEGRAM_CHAT_ID

def telegram_notify(message):

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    send_with_retry(TELEGRAM_URL, payload)