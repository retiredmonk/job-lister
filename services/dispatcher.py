from utils.logger import get_logger
from notifiers.slack import slack_notify
from notifiers.telegram import telegram_notify
from notifiers.discord import discord_notify

logger = get_logger()

def notify(message):
    notifiers = [
        ("slack", slack_notify),
        ("telegram", telegram_notify),
        ("discord", discord_notify)
    ]

    success_count = 0
    total = len(notifiers)

    results = {
        "success_count": 0,
        "total": total,
        "status": {}
    }

    for name, notifier in notifiers:
        try:
            sent = notifier(message)

            if sent:
                logger.info(f"Successfully notified {name}")
                success_count += 1
                results["status"][name] = True
            else:
                logger.error(f"Failed to notify {name}")
                results["status"][name] = False

        except Exception as e:
            logger.exception(f"Unexpected error while notifying {name}: {e}")
            results["status"][name] = False

    results["success_count"] = success_count

    return results