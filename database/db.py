import psycopg2
from services.config_service import *


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=10
    )

def init_db(connection):

    cursor = connection.cursor()

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

    connection.commit()
    cursor.close()


def add_details(connection, job):

    cursor = connection.cursor()

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

    cursor.close()

    return result is not None

def is_db_empty(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM job_list")

    count = cursor.fetchone()[0]

    cursor.close()

    return count == 0