from services.message_builder import build_message
from services.normalizer import normalize_all_jobs
from clients.rise import fetch_rise
from clients.arbeit_now import fetch_arbeit_now
from services.dispatcher import notify
from database.db import is_db_empty, add_details
from utils.logger import get_logger

logger = get_logger()

def run_pipeline():

    db_empty = is_db_empty()

    rise_jobs = fetch_rise()
    arbeit_jobs = fetch_arbeit_now()

    rise_jobs = rise_jobs or []
    arbeit_jobs = arbeit_jobs or []

    normalized_jobs = normalize_all_jobs(rise_jobs, arbeit_jobs)

    new_jobs = []

    for job in normalized_jobs:
        is_new = add_details(job)
        if not is_new:
            continue

        new_jobs.append(job)


    if not db_empty:

        if new_jobs:
            message = build_message(new_jobs)
            result = notify(message)

            success_count = result["success_count"]
            total = result["total"]

            if success_count == 0:
                logger.critical("All notifications failed. System may require attention.")
            elif success_count < total:
                failed_platforms = [
                    name for name, status in result["status"].items() if not status
                ]
                logger.warning(f"Partial failure. Failed platforms: {failed_platforms}")
            else:
                logger.info("All notifications sent successfully.")
        else:
            logger.info(f"No new jobs found. ({len(normalized_jobs)} already tracked)")