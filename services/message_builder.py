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

def build_combined_message(jobs):
    jobs = jobs[:10]
    message = f"🚨 {len(jobs)} New Job(s) Found\n\n"

    for i, job in enumerate(jobs, start=1):
        message += (
            f"{i}. {job['title']} — {job['company']}\n"
            f"   📍 {job['location']} | {job['job_type']}\n"
            f"   🔗 {job['url']}\n\n"
        )

    return message.strip()