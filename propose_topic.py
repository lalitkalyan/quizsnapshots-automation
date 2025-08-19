"""
propose_topic.py
-----------------

This script selects the next topic from the publish queue and requests
approval from the user via Telegram. It reads from ``data/publish_queue.csv``
and updates the status of the selected row to ``APPROVED_TOPIC`` if the
user approves. If the user rejects the proposed topic, the script
advances to the next topic in the queue.

Usage:

    python propose_topic.py

Environment variables:
    TELEGRAM_BOT_TOKEN: token for your Telegram bot

Configuration files:
    config/ops.yml
    config/status_keys.yml
"""

import csv
import os
from pathlib import Path
from typing import List

import yaml

# Placeholder Telegram send/receive functions. Replace with actual
# telegram bot API calls for production use.
def send_telegram_message(chat_id: str, text: str, buttons: List[str]) -> str:
    """Send a message with buttons and return the user's response."""
    print(f"[TELEGRAM] To {chat_id}: {text} (options: {buttons})")
    # Simulate a positive response for testing; in real use, wait for reply
    return 'Yes'

def propose_next_topic(queue_path: Path, chat_id: str) -> None:
    """Propose topics until approved or queue is exhausted."""
    with queue_path.open(newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))

    for row in rows:
        if row.get('status') == 'PLANNED':
            topic = row['topic']
            response = send_telegram_message(
                chat_id,
                f"Proposed topic: {topic}. Approve?",
                buttons=['Yes', 'No'],
            )
            if response.lower() == 'yes':
                row['status'] = 'APPROVED_TOPIC'
                break
            else:
                continue

    # Write updated statuses back to CSV
    with queue_path.open('w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def main() -> None:
    base = Path(__file__).resolve().parent.parent
    ops_path = base / 'config' / 'ops.yml'
    queue_path = base / 'data' / 'publish_queue.csv'
    with ops_path.open() as f:
        ops = yaml.safe_load(f)
    chat_id = ops['telegram']['chat_id']
    propose_next_topic(queue_path, chat_id)

if __name__ == '__main__':
    main()
