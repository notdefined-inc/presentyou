#!/usr/bin/env python3
"""
Read the content of a specific slide number.
"""
import argparse
import sys
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no", type=int, required=True, help="Slide number to read")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    
    # Simple check for filename pattern 00N.md
    filename = f"{args.no:03d}.md"
    path = root / "slides" / filename
    
    if not path.exists():
        print(f"Error: Slide {args.no} not found at {filename}")
        sys.exit(1)

    print(f"--- Slide {args.no} ({filename}) ---")
    print(path.read_text(encoding="utf-8"))

if __name__ == "__main__":
    main()
