from services.fetcher import fetch_with_retry

def fetch_rise():
    headers = {
    'content-type': 'application/json',
    'User-Agent': "job_lister/v1.0"
    }
    url = "https://api.joinrise.io/api/v1/jobs/public"

    return fetch_with_retry(url, headers=headers)