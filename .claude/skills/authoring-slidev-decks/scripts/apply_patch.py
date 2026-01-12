#!/usr/bin/env python3
"""
Apply a SlidePatch JSON to a Slidev project's slides directory.

Usage:
    python apply_patch.py patch.json --project ./my-presentation
    python apply_patch.py --stdin --project ./my-presentation
"""
from __future__ import annotations
import json
import sys
import base64
from pathlib import Path
from typing import Any, Dict, Optional


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
        if not b64:
            return
        out.write_bytes(base64.b64decode(b64))
    elif kind == "text":
        out.write_text(asset.get("text", ""), encoding="utf-8")
    elif kind == "copy":
        src = asset.get("from_path")
        if src:
            srcp = (root / src).resolve()
            if srcp.exists():
                out.write_bytes(srcp.read_bytes())


def render_slide(frontmatter: Dict[str, Any], content_md: str, notes_md: Optional[str]) -> str:
    """Render slide content to markdown format."""
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
        description="Apply a slide patch to a Slidev project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python apply_patch.py patch.json --project ./my-deck
  python apply_patch.py --stdin --project ./my-deck < patch.json
        """
    )
    parser.add_argument("patch_path", nargs="?", help="Path to patch JSON file")
    parser.add_argument("--stdin", action="store_true", help="Read patch from stdin")
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

    # Read patch content
    content = ""
    if args.stdin:
        content = sys.stdin.read()
    elif args.patch_path:
        patch_file = Path(args.patch_path)
        if not patch_file.exists():
            print(f"❌ Error: Patch file not found: {patch_file}")
            sys.exit(1)
        content = patch_file.read_text(encoding="utf-8")
    else:
        print("❌ Error: Provide a patch.json path or use --stdin")
        parser.print_help()
        sys.exit(1)

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)

    # Handle wrapped patch object
    patch = data.get("patch", data)

    no = int(patch["no"])
    fn = patch.get("filename") or f"{no:03d}.md"
    
    # Write assets to project
    for a in patch.get("assets", []) or []:
        write_asset(project_root, a)

    # Write slide to project/slides/
    slides_dir = project_root / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    out = slides_dir / fn
    
    out.write_text(
        render_slide(
            frontmatter=patch.get("frontmatter", {}) or {},
            content_md=patch.get("content_md", "") or "",
            notes_md=patch.get("notes_md"),
        ),
        encoding="utf-8",
    )
    print(f"✅ Patched slide {no} -> {out}")


if __name__ == "__main__":
    main()
