import logging
import time
from env import get_settings
from utils.errors import APIRateLimitedError, NetworkError, APIResponseError
from orchestrator.controller import run_pipeline
from utils.logger import setup_logging

config = get_settings()
poll_interval = config.POLL_INTERVAL

def main():
    setup_logging()

    try:
        while True:
            try:
                run_pipeline()
            except APIRateLimitedError as e:
                logging.error(f"Rate limit error: {e}")
            except NetworkError as e:
                logging.error(f"Network error: {e}")
            except APIResponseError as e:
                logging.error(f"API error: {e}")
            except Exception as e:
                logging.exception(f"Unexpected crash: {e}")

            logging.info(f"Sleeping for {poll_interval} seconds...\n")
            time.sleep(poll_interval)
            
    except KeyboardInterrupt:
        logging.info("User triggered shutdown. Shutting down...")

if __name__ == "__main__":
    main()