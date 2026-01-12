#!/usr/bin/env python3
"""
Audit the deck for common issues.

Usage:
    python audit.py --project ./my-presentation
"""
import json
import re
import sys
import argparse
from pathlib import Path

def main() -> None:
    parser = argparse.ArgumentParser(description="Audit Slidev project")
    parser.add_argument("--project", "-p", required=True, help="Path to Slidev project")
    args = parser.parse_args()

    project_root = Path(args.project).resolve()
    if not project_root.exists():
        print(f"❌ Error: Project directory not found: {project_root}")
        sys.exit(1)

    issues = []
    warnings = []

    # Check slides.md exists
    slides_md = project_root / "slides.md"
    if not slides_md.exists():
        issues.append("❌ Missing slides.md")
    else:
        # Check referenced files exist
        content = slides_md.read_text(encoding="utf-8")
        refs = re.findall(r"src:\s+(\S+)", content)
        if not refs:
            issues.append("❌ No 'src:' slide references found in slides.md")

        seen = set()
        for ref in refs:
            if ref in seen:
                warnings.append(f"⚠️  Duplicate reference in slides.md: {ref}")
            seen.add(ref)

            # ref is relative to slides.md usually
            p = (project_root / ref).resolve()
            if not p.exists():
                issues.append(f"❌ broken link in slides.md: {ref}")

        # Warn about unreferenced slides
        slides_dir = project_root / "slides"
        if slides_dir.exists():
            slide_files = {f"./slides/{p.name}" for p in slides_dir.glob("*.md")}
            unreferenced = sorted(slide_files - set(refs))
            if unreferenced:
                warnings.append(f"⚠️  Unreferenced slide files in ./slides/: {', '.join(unreferenced)}")

        # If deck.json exists, compare expected ordering to slides.md
        deck_json = project_root / "deck.json"
        if deck_json.exists():
            try:
                data = json.loads(deck_json.read_text(encoding="utf-8"))
                deck = data.get("deck", data)
                slides = deck.get("slides", []) or []
                expected: list[str] = []
                for s in sorted(slides, key=lambda x: int(x.get("no", 0))):
                    no = int(s.get("no", 0))
                    fn = s.get("filename") or f"{no:03d}.md"
                    expected.append(f"./slides/{fn}")
                if expected and refs and expected != refs:
                    warnings.append("⚠️  slides.md order differs from deck.json (expected src list does not match).")
            except Exception as e:
                warnings.append(f"⚠️  Could not parse deck.json for comparison: {e}")

    if issues:
        print("\n".join(issues + warnings))
        sys.exit(1)
    else:
        if warnings:
            print("\n".join(warnings))
        print("✅ Audit passed. Deck structure looks good.")

if __name__ == "__main__":
    main()
