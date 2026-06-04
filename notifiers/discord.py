from env import get_settings
from services.notifier import send_with_retry

config = get_settings()

def discord_notify(message):

    url = f"https://discord.com/api/webhooks/{config.DISCORD_ID}/{config.DISCORD_TOKEN}"

    payload = {
        "content": message
    }

    return send_with_retry(url, payload, json_mode=True)
