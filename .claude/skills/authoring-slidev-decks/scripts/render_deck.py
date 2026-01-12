#!/usr/bin/env python3
"""
Render a full deck.json to a Slidev project's slides directory.

Usage:
    python render_deck.py deck.json --project ./my-presentation
    python render_deck.py --stdin --project ./my-presentation
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import base64


def to_yaml(obj: dict) -> str:
    import yaml
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True).strip()


def write_asset(root: Path, asset: Dict[str, Any]) -> None:
    """Write an asset (base64, text, or copy) to the project."""
    rel = asset["path"]
    out = (root / rel).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    kind = asset["kind"]
    if kind == "base64":
        b64 = asset.get("base64")
        if b64:
            out.write_bytes(base64.b64decode(b64))
    elif kind == "text":
        out.write_text(asset.get("text", ""), encoding="utf-8")
    elif kind == "copy":
        src = asset.get("from_path")
        if src:
            srcp = (root / src).resolve()
            if srcp.exists():
                out.write_bytes(srcp.read_bytes())


def render_slide_file(frontmatter: Dict[str, Any], content_md: str, notes_md: Optional[str]) -> str:
    """Render a single slide to markdown format."""
    parts = ["---"]
    if frontmatter:
        parts.append(to_yaml(frontmatter))
    parts.append("---")
    parts.append(content_md.strip() + "\n")
    if notes_md and notes_md.strip():
        parts.append("<!--")
        parts.append(notes_md.strip())
        parts.append("-->")
    return "\n".join(parts).strip() + "\n"


def validate_project(project_path: Path) -> bool:
    """Validate that the project directory is a valid Slidev project."""
    if not project_path.exists():
        print(f"❌ Error: Project directory does not exist: {project_path}")
        return False
    if not (project_path / "package.json").exists():
        print(f"❌ Error: No package.json found in {project_path}")
        print("   Hint: Initialize a Slidev project first with init_slidev_project.py")
        return False
    return True


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(
        description="Render a deck.json to a Slidev project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python render_deck.py deck.json --project ./my-deck
  python render_deck.py --stdin --project ./my-deck < deck.json
        """
    )
    parser.add_argument("deck_path", nargs="?", help="Path to deck.json file")
    parser.add_argument("--stdin", action="store_true", help="Read deck.json from stdin")
    parser.add_argument(
        "--project", "-p",
        required=True,
        help="Path to target Slidev project directory (required)"
    )
    args = parser.parse_args()

    # Resolve and validate project path
    project_root = Path(args.project).resolve()
    if not validate_project(project_root):
        sys.exit(1)

    # Read deck content
    content = ""
    if args.stdin:
        content = sys.stdin.read()
    elif args.deck_path:
        deck_file = Path(args.deck_path)
        if not deck_file.exists():
            print(f"❌ Error: Deck file not found: {deck_file}")
            sys.exit(1)
        content = deck_file.read_text(encoding="utf-8")
    else:
        print("❌ Error: Provide a deck.json path or use --stdin")
        parser.print_help()
        sys.exit(1)

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)

    # Handle wrapped deck object
    deck_obj = data.get("deck", data)
    headmatter = deck_obj.get("headmatter", {})
    slides = deck_obj.get("slides", [])

    if not slides:
        print("❌ Error: No slides found in deck.json")
        sys.exit(1)

    # Write assets to project
    for s in slides:
        for a in s.get("assets", []) or []:
            write_asset(project_root, a)

    # Write slides to project/slides/
    slides_dir = project_root / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)

    max_no = 0
    for s in slides:
        no = int(s["no"])
        max_no = max(max_no, no)
        fn = s.get("filename") or f"{no:03d}.md"
        out = slides_dir / fn
        out.write_text(
            render_slide_file(
                frontmatter=s.get("frontmatter", {}) or {},
                content_md=s.get("content_md", "") or "",
                notes_md=s.get("notes_md"),
            ),
            encoding="utf-8",
        )
        print(f"  ✅ Wrote {fn}")

    # Rebuild slides.md entry point
    entry_lines: List[str] = []
    entry_lines.append("---")
    entry_lines.append(to_yaml(headmatter).strip() if headmatter else "")
    entry_lines.append("---")
    entry_lines.append("")
    entry_lines.append(f"# {headmatter.get('title', 'Slidev Deck')}")
    entry_lines.append("")
    entry_lines.append("> Auto-generated. Do not hand-edit if you are using the JSON pipeline.")
    entry_lines.append("")

    for no in range(1, max_no + 1):
        fn = f"{no:03d}.md"
        entry_lines.append("---")
        entry_lines.append(f"src: ./slides/{fn}")
        entry_lines.append("---")
        entry_lines.append("")

    slides_md_path = project_root / "slides.md"
    slides_md_path.write_text("\n".join(entry_lines).rstrip() + "\n", encoding="utf-8")
    
    print(f"\n✨ Rendered {len(slides)} slide(s) -> {slides_md_path}")


if __name__ == "__main__":
    main()
