from env import get_settings
from services.notifier import send_with_retry

config = get_settings()

def telegram_notify(message):

    url = f'https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage'

    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": message
    }

    return send_with_retry(url, payload)