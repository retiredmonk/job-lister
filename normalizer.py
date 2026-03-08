from datetime import datetime

def normalize_rise_jobs(rise_jobs):

    normalized_jobs=[]
    for job in rise_jobs:
        normalized_job = {
            "title": job.get('title'),
            "company": job.get("owner", {}).get("companyName"),
            "location": job.get('locationAddress'),
            "job_type" : job.get('workModel'),
            "url" : str(job.get('url')),
            "source" : 'Rise',
            "date" : datetime.fromisoformat(job.get("createdAt").replace("Z", "+00:00")).date()
        }
        normalized_jobs.append(normalized_job)

    return normalized_jobs

def normalize_arbeit_jobs(arbeit_jobs):

    normalized_jobs=[]
    for job in arbeit_jobs:
        normalized_job = {
            "title": job.get('title'),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "job_type" : str(job.get("remote")),
            "url" : str(job.get("url")),
            "source" : 'Arbeit Now',
            "date" : datetime.utcfromtimestamp(job.get("created_at")).date()
        }
        normalized_jobs.append(normalized_job)

    return normalized_jobs

def normalize_all_jobs(rise_jobs, arbeit_jobs):

    normalized_jobs = []

    normalized_jobs.extend(normalize_rise_jobs(rise_jobs))
    normalized_jobs.extend(normalize_arbeit_jobs(arbeit_jobs))

    return normalized_jobs

