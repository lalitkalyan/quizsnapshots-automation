"""
preview_approval.py
-------------------

This script sends a preview of generated questions to the user for
approval. It bundles sample frames (placeholder paths), the full list
of questions and answers, and the estimated runtime. The user can
either approve to proceed to rendering or reject to choose a different
topic. This simplified version reads questions from a JSONL file and
sends a static message via Telegram.

Usage:

    python preview_approval.py --questions questions.jsonl
"""

import argparse
import json
from pathlib import Path

def send_preview(chat_id: str, questions: list, estimated_runtime: int) -> str:
    """Send a preview to Telegram and return the user's response."""
    print(f"[TELEGRAM] Previewing {len(questions)} questions (runtime ≈ {estimated_runtime}s). Options: Proceed/Reject")
    # Always approve for this placeholder
    return 'Proceed'

def main() -> None:
    parser = argparse.ArgumentParser(description="Send a preview for approval.")
    parser.add_argument('--questions', required=True, help='Path to the questions JSONL file')
    parser.add_argument('--chat_id', default='REPLACE_WITH_CHAT_ID', help='Telegram chat ID')
    args = parser.parse_args()

    # Load questions
    questions = []
    with Path(args.questions).open() as f:
        for line in f:
            questions.append(json.loads(line))
    # Estimate runtime: 7s per question + 2s buffer
    estimated_runtime = len(questions) * 7 + 2
    response = send_preview(args.chat_id, questions, estimated_runtime)
    print(f"User response: {response}")

if __name__ == '__main__':
    main()
