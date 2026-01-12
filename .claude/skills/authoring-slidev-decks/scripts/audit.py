#!/usr/bin/env python3
"""
Audit the deck for common issues.

Usage:
    python audit.py --project ./my-presentation
"""
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

    # Check slides.md exists
    slides_md = project_root / "slides.md"
    if not slides_md.exists():
        issues.append("❌ Missing slides.md")
    else:
        # Check referenced files exist
        content = slides_md.read_text(encoding="utf-8")
        refs = re.findall(r"src:\s+(\S+)", content)
        for ref in refs:
            # ref is relative to slides.md usually
            p = (project_root / ref).resolve()
            if not p.exists():
                issues.append(f"❌ broken link in slides.md: {ref}")

    if issues:
        print("\n".join(issues))
        sys.exit(1)
    else:
        print("✅ Audit passed. Deck structure looks good.")

if __name__ == "__main__":
    main()
