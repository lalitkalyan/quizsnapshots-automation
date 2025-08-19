"""
analytics.py
-------------

This script pulls analytics for recently published videos and triggers
optimizations if performance thresholds are not met. In this placeholder
version, it simply prints a summary of PUBLISHED entries from
``publish_queue.csv`` without performing any optimizations.

Usage:

    python analytics.py

Configuration files:
    config/ops.yml

Data files:
    data/publish_queue.csv
"""

import csv
from pathlib import Path

def summarize_published(queue_path: Path) -> None:
    with queue_path.open(newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))
    published = [row for row in rows if row.get('status') == 'PUBLISHED']
    if not published:
        print("No published videos to analyze.")
        return
    print("Published videos:")
    for row in published:
        print(f"- {row['topic']} (published at {row.get('published_at')})")


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    queue_path = base / 'data' / 'publish_queue.csv'
    summarize_published(queue_path)

if __name__ == '__main__':
    main()
