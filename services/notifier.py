import requests
import random
import time
from utils.logger import get_logger

logger = get_logger()

def send_with_retry(url, payload, json_mode=False):

    base = 2
    max_retries = 3

    for attempt in range(1, max_retries + 1):

        try:
            if json_mode:
                response = requests.post(url=url, json=payload, timeout=10.0)
            else:
                response = requests.post(url=url, data=payload, timeout=10.0)

            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
            wait = random.uniform(0, base * 2 ** attempt)
            logger.error(f"Notification failed due to error {str(e)}, retrying in {wait} seconds.")
            time.sleep(wait)

    logger.error("Failed to send notification after max retries.")
    return False