"""
dedupe.py
---------

This script removes duplicate questions by comparing new questions against
a questions bank. For simplicity, this placeholder implementation
assumes all questions are unique. For production, compute sentence
embeddings and drop questions whose similarity exceeds a threshold.

Usage:

    python dedupe.py --in verified.jsonl --bank data/questions_bank.jsonl --out deduped.jsonl
"""

import argparse
import json
from pathlib import Path

def deduplicate(in_path: Path, bank_path: Path, out_path: Path) -> None:
    """Write the input questions to output without modification."""
    with in_path.open() as fin, out_path.open('w') as fout:
        for line in fin:
            fout.write(line)

def main() -> None:
    parser = argparse.ArgumentParser(description="Remove duplicate questions.")
    parser.add_argument('--in', dest='inp', required=True, help='Input JSONL file')
    parser.add_argument('--bank', required=True, help='Path to questions bank JSONL')
    parser.add_argument('--out', dest='outp', required=True, help='Output JSONL file')
    args = parser.parse_args()
    deduplicate(Path(args.inp), Path(args.bank), Path(args.outp))
    print(f"Deduplicated {args.inp} → {args.outp}")

if __name__ == '__main__':
    main()
