#!/usr/bin/env python3
"""
List all slides with their titles.
"""
import re
from pathlib import Path

def get_title(content: str) -> str:
    # Find first markdown heading
    m = re.search(r"^#\s+(.*)", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return "(No title)"

def main() -> None:
    root = Path(__file__).resolve().parents[1]
    slides_dir = root / "slides"
    
    if not slides_dir.exists():
        print("No slides directory found.")
        return

    files = sorted(slides_dir.glob("*.md"))
    if not files:
        print("No slides found.")
        return

    print(f"{'No':<5} {'File':<10} {'Title'}")
    print("-" * 40)
    
    for f in files:
        # Try to infer number from filename
        try:
            no = int(f.stem)
        except ValueError:
            no = -1
        
        content = f.read_text(encoding="utf-8")
        title = get_title(content)
        print(f"{no:<5} {f.name:<10} {title}")

if __name__ == "__main__":
    main()
