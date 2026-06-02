from .utility import send_with_retry
from services.config_service import DISCORD_URL

def discord_notify(message):

    payload = {
        "content": message
    }

    send_with_retry(DISCORD_URL, payload, json_mode=True)