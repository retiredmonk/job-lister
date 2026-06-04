# Job-Lister

A polling bot that aggregates remote job listings from multiple APIs, deduplicates them via PostgreSQL, and pushes alerts to Slack, Telegram, and Discord.

## What it does

- Fetches jobs from **Rise** and **Arbeit Now** on a configurable interval
- Normalizes and deduplicates listings against a PostgreSQL database
- Sends a combined alert to all configured notification channels
- Handles rate limits, server errors, and network failures with exponential backoff retry
- Gracefully degrades if one or more notification channels fail

## Project Structure

```
Job-Lister/
├── main.py                  # Entry point, poll loop
├── orchestrator/
│   └── controller.py        # Pipeline orchestration
├── clients/
│   ├── rise.py              # Rise API client
│   └── arbeit_now.py        # Arbeit Now API client
├── services/
│   ├── fetcher.py           # Shared HTTP fetch with retry
│   ├── notifier.py          # Shared HTTP notify with retry
│   ├── normalizer.py        # Job normalization across sources
│   ├── dispatcher.py        # Fan-out to all notifiers
│   └── message_builder.py   # Message formatting
├── notifiers/
│   ├── slack.py
│   ├── telegram.py
│   └── discord.py
├── database/
│   └── db.py                # PostgreSQL connection and queries
└── utils/
    ├── logger.py
    └── errors.py
```

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=your_db_user
DB_PASSWORD=your_db_password

DISCORD_ID=your_webhook_id
DISCORD_TOKEN=your_webhook_token

TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

SLACK_URL=https://hooks.slack.com/services/...

POLL_INTERVAL=120
```

### Initialize the database

```bash
python -c "from database.db import init_db; init_db()"
```

### Run

```bash
python main.py
```

## Behavior

On the **first run**, the bot populates the database without sending notifications — this prevents a flood alert from all historically listed jobs. On every subsequent run, only newly seen jobs trigger alerts.

If all three notification channels fail, the bot logs a `CRITICAL` warning and continues polling rather than crashing.

## Retry Logic

Both API fetching and notification delivery use exponential backoff with jitter:

- Max 3 attempts
- Wait time: `random(0, 2 * 2^attempt)` seconds
- 429 and 5xx responses are retried; 4xx client errors fail immediately

## Logs

Logs are written to `logs/job_lister.log` and mirrored to stdout.