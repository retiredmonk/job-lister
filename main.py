from config import *
import logging
from errors import *
from normalizer import *
from api_clients.rise import fetch_rise
from api_clients.arbeit_now import fetch_arbeit_now
from database.db import init_db, add_details, get_connection
from notifiers.telegram import telegram_notify
from notifiers.discord import discord_notify
from notifiers.slack import slack_notify
import time


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_FILE)
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def build_message(job):
    return f"""
    🚨 Job Alert ({job['source']})

    Title: {job['title']}
    Company: {job['company']}
    Location: {job['location']}
    Type: {job['job_type']}
    Date: {job['date']}

    Apply: {job['url']}
    """

first_run = True

def run_pipeline(conn):
    global first_run

    rise_jobs = fetch_rise()
    arbeit_jobs = fetch_arbeit_now()

    normalized_jobs = normalize_all_jobs(rise_jobs, arbeit_jobs)

    new_jobs = []

    for job in normalized_jobs:

        is_new = add_details(conn, job)

        if is_new:
            new_jobs.append(job)

    conn.commit()

    for job in new_jobs:
        message = build_message(job)

        telegram_notify(message)
        slack_notify(message)
        discord_notify(message)

    first_run = False

def main():
    setup_logging()

    conn = get_connection()
    init_db(conn)

    poll_interval = POLL_INTERVAL

    while True:
        try:
            run_pipeline(conn)

        except KeyboardInterrupt:
            logging.info("User triggered Shutdown, Shutting down...")
            conn.close()

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


if __name__ == "__main__":
    main()