def build_message(jobs):
    jobs = jobs[:10]
    message = f"🚨 {len(jobs)} New Job(s) Found\n\n"

    for i, job in enumerate(jobs, start=1):
        message += (
            f"{i}. {job['title']} — {job['company']}\n"
            f"   📍 {job['location']} | {job['job_type']}\n"
            f"   🔗 {job['url']}\n\n"
        )

    return message.strip()