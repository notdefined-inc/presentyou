#!/usr/bin/env python3
"""
Introspect a local Slidev project (node_modules) for:
- Built-in layouts
- Built-in transitions
- Headmatter/frontmatter keys
- Built-in components/directives

Usage:
  python slidev_introspect.py --project ./my-deck
  python slidev_introspect.py --project ./my-deck --format json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_union_literals(text: str, type_name: str) -> list[str]:
    m = re.search(rf"type\s+{re.escape(type_name)}\s*=\s*([^;]+);", text)
    if not m:
        return []
    return re.findall(r"'([^']+)'", m.group(1))


def extract_interface_block(text: str, interface_name: str) -> str | None:
    start = text.find(f"interface {interface_name}")
    if start < 0:
        return None

    brace_start = text.find("{", start)
    if brace_start < 0:
        return None

    depth = 0
    for i in range(brace_start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[brace_start + 1 : i]
    return None


def extract_interface_keys(block: str) -> list[str]:
    keys: list[str] = []
    for raw in block.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(("/", "*")):
            continue

        m = re.match(r"([A-Za-z0-9_]+)\??\s*:", line)
        if not m:
            continue
        key = m.group(1)
        keys.append(key)

    # keep stable ordering but de-dupe
    seen: set[str] = set()
    out: list[str] = []
    for k in keys:
        if k in seen:
            continue
        seen.add(k)
        out.append(k)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Introspect Slidev options from node_modules")
    ap.add_argument("--project", "-p", required=True, help="Path to Slidev project directory")
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = ap.parse_args()

    project_root = Path(args.project).resolve()
    if not (project_root / "package.json").exists():
        print(f"❌ Error: Not a Slidev project (missing package.json): {project_root}")
        sys.exit(1)

    types_file = project_root / "node_modules" / "@slidev" / "types" / "dist" / "index.d.mts"
    client_builtin_dir = project_root / "node_modules" / "@slidev" / "client" / "builtin"
    cli_pkg = project_root / "node_modules" / "@slidev" / "cli" / "package.json"

    missing = []
    if not types_file.exists():
        missing.append(str(types_file))
    if not client_builtin_dir.exists():
        missing.append(str(client_builtin_dir))
    if missing:
        print("❌ Error: Slidev dependencies not found in node_modules.")
        print("  Run `npm install` in the project first.")
        for m in missing:
            print(f"  Missing: {m}")
        sys.exit(1)

    types_text = types_file.read_text(encoding="utf-8")
    layouts = extract_union_literals(types_text, "BuiltinLayouts")
    transitions = extract_union_literals(types_text, "BuiltinSlideTransition")

    headmatter_block = extract_interface_block(types_text, "HeadmatterConfig") or ""
    frontmatter_block = extract_interface_block(types_text, "Frontmatter") or ""
    headmatter_keys = extract_interface_keys(headmatter_block) if headmatter_block else []
    frontmatter_keys = extract_interface_keys(frontmatter_block) if frontmatter_block else []

    components: list[str] = []
    directives: list[str] = []
    for p in sorted(client_builtin_dir.iterdir()):
        if p.suffix not in {".vue", ".ts"}:
            continue
        name = p.stem
        if name.startswith("V") and p.suffix == ".ts":
            directives.append(name)
        else:
            components.append(name)

    versions: dict[str, Any] = {}
    if cli_pkg.exists():
        try:
            versions["@slidev/cli"] = read_json(cli_pkg).get("version")
        except Exception:
            pass

    payload: dict[str, Any] = {
        "project": str(project_root),
        "versions": versions,
        "builtin": {
            "layouts": layouts,
            "transitions": transitions,
            "headmatter_keys": headmatter_keys,
            "frontmatter_keys": frontmatter_keys,
            "components": components,
            "directives": directives,
            "sources": {
                "types": str(types_file),
                "builtin_components": str(client_builtin_dir),
            },
        },
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    # markdown output
    print("# Slidev Introspection\n")
    if versions:
        print("## Versions")
        for k, v in versions.items():
            print(f"- {k}: {v}")
        print()

    print("## Built-in Layouts")
    for l in layouts:
        print(f"- `{l}`")
    print()

    print("## Built-in Transitions")
    for t in transitions:
        print(f"- `{t}`")
    print()

    print("## Headmatter Keys (Presentation-level)")
    for k in headmatter_keys:
        print(f"- `{k}`")
    print()

    print("## Frontmatter Keys (Slide-level)")
    for k in frontmatter_keys:
        print(f"- `{k}`")
    print()

    print("## Built-in Components")
    for c in components:
        print(f"- `<{c} />`")
    print()

    print("## Built-in Directives")
    for d in directives:
        print(f"- `{d}`")
    print()

    print("## Sources")
    print(f"- Types: `{types_file}`")
    print(f"- Builtins: `{client_builtin_dir}`")


if __name__ == "__main__":
    main()

