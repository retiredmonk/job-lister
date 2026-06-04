import requests
import random
import time
from utils.errors import APIResponseError
from utils.logger import get_logger

logger = get_logger()

def fetch_with_retry(url, headers):

    base = 2
    max_retries = 3

    saw_rate_limit = False
    saw_network_error = False
    saw_server_error = False

    for attempt in range(1, max_retries+1):
        wait = random.uniform(0, base * 2 ** attempt)

        try:
            response = requests.get(url, headers=headers, timeout=10.0)

            if response.status_code == 429:
                saw_rate_limit = True
                logger.info(f"Rate limit reached, waiting {str(wait)} seconds")
                time.sleep(wait)
                continue

            if 500 <= response.status_code < 600:
                saw_server_error = True
                logger.info(f"Server Error, waiting {str(wait)} seconds")
                time.sleep(wait)
                continue

            if 400 <= response.status_code < 500 and response.status_code != 429:
                logger.info(f"Client error, waiting {str(wait)} seconds")
                time.sleep(wait)
                break

            data = response.json()

            if isinstance(data, dict) and data.get("message"):
                logger.error(f"API error: {data}")
                return None

            logger.info("Data Retrieved successfully")

            return data.get("data", [])


        except requests.exceptions.RequestException as e:
            logger.warning(f"Network error: {e}. Retrying in {wait}s for (attempt {attempt})")
            time.sleep(wait)
            saw_network_error = True

        except ValueError as e:
            logger.error(f"Data validation error: {e}")
            raise APIResponseError(f"Data validation error: {e}")

        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            raise APIResponseError(f"Unexpected error: {e}")

    if saw_rate_limit:
        logger.error("Rate limit reached after retries")

    elif saw_network_error:
        logger.critical("Network error persisted after retries")

    elif saw_server_error:
        logger.error("Server error persisted after retries")

    else:
        logger.critical("API failed after maximum retries")

    return None
