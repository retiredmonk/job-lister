import requests, logging, random, time
from services.config_service import EXPONENTIAL_BASE, EXPONENTIAL_MAX_RETRIES, TIMEOUT

def send_with_retry(url, payload, json_mode=False):

    base = EXPONENTIAL_BASE
    max_retries = EXPONENTIAL_MAX_RETRIES

    for attempt in range(1, max_retries + 1):

        try:
            if json_mode:
                response = requests.post(url=url, json=payload, timeout=TIMEOUT)
            else:
                response = requests.post(url=url, data=payload, timeout=TIMEOUT)

            response.raise_for_status()
            return True

        except requests.exceptions.RequestException as e:
            wait = random.uniform(0, base * 2 ** attempt)
            logging.error(f"Notification failed. Retrying in {wait} seconds.")
            time.sleep(wait)

    logging.error("Failed to send notification after retries.")
    return False