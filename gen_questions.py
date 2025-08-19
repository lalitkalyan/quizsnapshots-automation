"""
gen_questions.py
-----------------

Generates multiple-choice questions (MCQs) for a given topic. The script
reads a topic entry from the publish queue that has been approved and
generates a set of questions that fit within the total runtime constraint
(45–59 seconds for a Short). The resulting questions are written to a
temporary JSON Lines file for downstream processing.

This is a simplified placeholder implementation that produces fixed
questions for demonstration purposes. In a production system, you
would integrate with an LLM or question database.

Usage:

    python gen_questions.py --topic "World Capitals" --out questions.jsonl

Configuration files:
    config/brand.yml
"""

import argparse
import json
from pathlib import Path

def generate_placeholder_questions(topic: str, n: int) -> list:
    """Generate n placeholder question dictionaries for a topic."""
    questions = []
    for i in range(1, n + 1):
        questions.append({
            'question': f'Placeholder question {i} about {topic}?',
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct': 0,
            'hint': '',
            'explanation': 'This is a placeholder question.'
        })
    return questions

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate placeholder MCQs.")
    parser.add_argument('--topic', required=True, help='Topic for the quiz')
    parser.add_argument('--n', type=int, default=3, help='Number of questions to generate')
    parser.add_argument('--out', type=str, default='questions.jsonl', help='Output JSONL file')
    args = parser.parse_args()

    questions = generate_placeholder_questions(args.topic, args.n)
    out_path = Path(args.out)
    with out_path.open('w') as f:
        for q in questions:
            f.write(json.dumps(q) + '\n')
    print(f"Generated {len(questions)} placeholder questions for {args.topic} → {out_path}")

if __name__ == '__main__':
    main()
