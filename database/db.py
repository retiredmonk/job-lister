import psycopg2
from env import get_settings

config = get_settings()

def get_connection():
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        connect_timeout=10
    )

def init_db():

    with get_connection() as conn:

        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_list (
                JOB_ID SERIAL PRIMARY KEY,
                TITLE TEXT NOT NULL,
                COMPANY TEXT NOT NULL,
                LOCATION TEXT,
                JOB_TYPE TEXT,
                URL TEXT NOT NULL UNIQUE,
                SOURCE TEXT,
                DATE DATE NOT NULL DEFAULT CURRENT_DATE
            )
        """)


def add_details(job):

    with get_connection() as conn:

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO job_list (title, company, location, url, source)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (url) DO NOTHING
            RETURNING url
            """,
            (
                job["title"],
                job["company"],
                job["location"],
                job["url"],
                job["source"]
            )
        )
        result = cursor.fetchone()

    return result is not None

def is_db_empty():

    with get_connection() as conn:

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM job_list")
        count = cursor.fetchone()[0]

    return count == 0

