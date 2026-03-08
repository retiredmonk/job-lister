import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Incoming APIs

RISE_URL = "https://api.joinrise.io/api/v1/jobs/public"

RISE_HEADERS = {
    'content-type': 'application/json',
    'User-Agent': "job_lister/v1.0"
} #not really necessary

RISE_PARAMS = {}


ARBEIT_NOW_URL = "https://www.arbeitnow.com/api/job-board-api"

ARBEIT_NOW_HEADERS = {
    'content-type': 'application/json',
    'User-Agent': "job_lister/v1.0"
}

ARBEIT_NOW_PARAMS = {}

# DATABASE

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

# LOGGING

LOG_DIR = Path('logs')
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR/"job_lister.log"

# ROBUST

EXPONENTIAL_BASE = 2
EXPONENTIAL_MAX_RETRIES = 3
TIMEOUT = 10
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL"))

#TELEGRAM

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

#DISCORD

DISCORD_BOT_TOKEN = os.getenv("DISCORD_TOKEN_ID")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_URL = f"https://discord.com/api/webhooks/{DISCORD_BOT_TOKEN}/{DISCORD_TOKEN}"

#SLACK

SLACK_URL = os.getenv("SLACK_URL")
