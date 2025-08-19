"""
buffer_watcher.py
-------------------

This module monitors the number of ready (rendered but unscheduled) videos
and triggers a refill process when the buffer falls below a low-watermark.

The script should be scheduled via cron or n8n. It reads the configured
thresholds from ``config/ops.yml`` and counts the number of items in
``data/publish_queue.csv`` that have status == "READY". If the count
falls below ``low_watermark``, it sends a notification via Telegram to
start producing more videos until ``target`` ready items are available.

You can run this script manually for testing:

    python buffer_watcher.py

Environment variables:
    TELEGRAM_BOT_TOKEN: token for your Telegram bot

Configuration files:
    config/ops.yml
"""

import csv
import json
import os
from pathlib import Path

import yaml

# Placeholder for Telegram bot integration. In a full implementation,
# you would import the telegram library and use it to send messages.
def send_telegram_message(chat_id: str, text: str) -> None:
    """Send a message via Telegram. Placeholder implementation."""
    print(f"[TELEGRAM] To {chat_id}: {text}")

def count_ready_items(queue_path: Path) -> int:
    """Count the number of entries with status == 'READY'."""
    if not queue_path.exists():
        return 0
    with queue_path.open(newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return sum(1 for row in reader if row.get('status') == 'READY')

def main() -> None:
    base = Path(__file__).resolve().parent.parent
    ops_path = base / 'config' / 'ops.yml'
    queue_path = base / 'data' / 'publish_queue.csv'

    # Load operational settings
    with ops_path.open('r') as f:
        ops = yaml.safe_load(f)

    low_watermark = ops['buffer']['low_watermark']
    target = ops['buffer']['target']
    chat_id = ops['telegram']['chat_id']

    ready_count = count_ready_items(queue_path)
    if ready_count < low_watermark:
        missing = target - ready_count
        message = (
            f"Only {ready_count} READY items left. Should I start generating "
            f"{missing} more to reach the target of {target}?"
        )
        send_telegram_message(chat_id, message)
    else:
        print(f"Buffer sufficient ({ready_count} READY items ≥ {low_watermark}).")

if __name__ == '__main__':
    main()
