from .utility import send_with_retry
from services.config_service import SLACK_URL

def slack_notify(message):

    payload = {
        "text": message
    }

    send_with_retry(SLACK_URL, payload, json_mode=True)