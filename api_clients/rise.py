import requests, logging, random, time
from services.config_service import *
from services.errors_service import *

def fetch_rise():
    headers = RISE_HEADERS
    params = RISE_PARAMS
    url = RISE_URL

    base = EXPONENTIAL_BASE
    max_retries = EXPONENTIAL_MAX_RETRIES
    timeout = TIMEOUT

    saw_rate_limit = False
    saw_network_error = False
    saw_server_error = False

    for attempt in range(1, max_retries+1):
        wait = random.uniform(0, base * 2 ** attempt)

        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)

            if response.status_code == 429:
                saw_rate_limit = True
                logging.info("Rate limit reached, waiting " + str(wait) + " seconds")
                time.sleep(wait)
                continue

            if 500 <= response.status_code < 600:
                saw_server_error = True
                logging.info("Server Error!, waiting " + str(wait) + " seconds")
                time.sleep(wait)
                continue

            if 400 <= response.status_code < 500:
                logging.info("Client error!, waiting " + str(wait) + " seconds")
                time.sleep(wait)
                continue

            data = response.json()
            logging.info("Successfully retrieved data")
            return data.get("data", [])

        except requests.exceptions.RequestException as e:
            logging.warning(f"Network error: {e}. Retrying in {wait}s for (attempt {attempt})")
            time.sleep(wait)
            saw_network_error = True

        except ValueError as e:
            logging.error(f"Data validation error: {e}")
            raise APIResponseError(f"Data validation error: {e}")

        except Exception as e:
            logging.exception(f"Unexpected error: {e}")
            raise APIResponseError(f"Unexpected error: {e}")

    if saw_rate_limit:
        logging.error("Rate limit reached, maximum retries reached")
        raise APIRateLimitedError("Rate limit reached, maximum retries reached")

    elif saw_network_error:
        logging.error("Network error occurred")
        raise NetworkError("Network error occurred")

    elif saw_server_error:
        logging.error("Server error occurred, maximum retries reached")
        raise NetworkError("Failed to connect to server, maximum retries reached")

    else:
        logging.critical("API failed after maximum retries")
        raise APIResponseError("Failed to retrieve data after maximum retries")