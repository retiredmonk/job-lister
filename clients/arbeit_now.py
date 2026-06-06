from services.fetcher import fetch_with_retry

def fetch_arbeit_now():
    headers = {
    'content-type': 'application/json',
    'User-Agent': "job_lister/v1.0"
    }

    url = "https://www.arbeitnow.com/api/job-board-api"

    return fetch_with_retry(url, headers)