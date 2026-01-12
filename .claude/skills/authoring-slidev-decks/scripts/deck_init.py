#!/usr/bin/env python3
"""
Initialize a Slidev deck structure.
"""
import argparse
import sys
from pathlib import Path
from textwrap import dedent

def write_file_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Created {path}")
    else:
        print(f"Exists {path}")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Overwrite existing files (careful!)")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    
    # Ensure slides directory exists
    (root / "slides").mkdir(parents=True, exist_ok=True)
    (root / "assets").mkdir(parents=True, exist_ok=True)
    (root / "checkpoints").mkdir(parents=True, exist_ok=True)
    (root / "exports").mkdir(parents=True, exist_ok=True)

    # Initial slides.md if missing
    slides_md = dedent("""
    ---
    theme: default
    title: "Slidev Deck"
    info: false
    presenter: true
    download: false
    selectable: true
    ---

    # Slidev Deck

    > Auto-generated entry point.

    ---

    src: ./slides/001.md
    ---
    """)
    
    dedent_slide1 = dedent("""
    ---
    layout: cover
    ---
    # Welcome
    ## Started with deck_init
    """)
    
    if args.force or not (root / "slides.md").exists():
        write_file_if_missing(root / "slides.md", slides_md)

    if args.force or not (root / "slides/001.md").exists():
        write_file_if_missing(root / "slides/001.md", dedent_slide1)

    print("Deck initialized.")

if __name__ == "__main__":
    main()
