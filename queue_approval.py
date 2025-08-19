"""
queue_approval.py
------------------

This script requests user approval to move a READY item into the
upload/scheduling queue. It scans ``data/publish_queue.csv`` for rows
with status ``READY`` and prompts the user via Telegram. If the user
approves, the status is updated to ``IN_QUEUE``. Otherwise, the item
remains READY.

Usage:

    python queue_approval.py

Environment variables:
    TELEGRAM_BOT_TOKEN

Configuration files:
    config/ops.yml
    config/status_keys.yml
"""

import csv
from pathlib import Path
from typing import List

import yaml


def send_queue_approval(chat_id: str, topic: str) -> str:
    """Send approval request to Telegram and return the user's response."""
    print(f"[TELEGRAM] Approve adding '{topic}' to the queue? Options: Add to Queue/Hold")
    # Placeholder: automatically approve
    return 'Add to Queue'

def queue_approval(queue_path: Path, chat_id: str) -> None:
    with queue_path.open(newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))
    updated = False
    for row in rows:
        if row.get('status') == 'READY':
            topic = row['topic']
            resp = send_queue_approval(chat_id, topic)
            if resp.lower().startswith('add'):
                row['status'] = 'IN_QUEUE'
            # Only prompt for the first READY item per run
            updated = True
            break
    if updated:
        with queue_path.open('w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

def main() -> None:
    base = Path(__file__).resolve().parent.parent
    ops_path = base / 'config' / 'ops.yml'
    with ops_path.open() as f:
        ops = yaml.safe_load(f)
    chat_id = ops['telegram']['chat_id']
    queue_path = base / 'data' / 'publish_queue.csv'
    queue_approval(queue_path, chat_id)

if __name__ == '__main__':
    main()
