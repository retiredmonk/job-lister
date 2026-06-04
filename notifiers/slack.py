from env import get_settings
from services.notifier import send_with_retry

config = get_settings()

def slack_notify(message):

    url = config.SLACK_URL

    payload = {
        "text": message
    }

    return send_with_retry(url, payload, json_mode=True)
