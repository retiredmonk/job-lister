from env import get_settings
from services.notifier import send_with_retry

config = get_settings()

def discord_notify(message):

    url = config.DISCORD_WEBHOOK_URL

    payload = {
        "content": message
    }

    return send_with_retry(url, payload, json_mode=True)
