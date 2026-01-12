#!/usr/bin/env python3
"""
Validate a JSON file against the deck or slide_patch schema.
Automatically detects which schema to use based on content.
"""
import argparse
import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

def validate_json(instance: dict, schema_path: Path) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=instance, schema=schema)


def _wrap_deck(data: dict) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    if "deck" in data:
        if "mode" not in data:
            warnings.append("Missing top-level 'mode'; assuming 'build' for validation.")
        return {"mode": data.get("mode", "build"), "deck": data["deck"]}, warnings

    if "headmatter" in data and "slides" in data:
        warnings.append("Input is a raw deck object; wrapping into {'mode':'build','deck':...} for validation.")
        return {"mode": "build", "deck": data}, warnings

    raise ValueError("Deck JSON must contain either {'deck': ...} or a raw {'headmatter': ..., 'slides': ...} object.")


def _wrap_patch(data: dict) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    if "patch" in data:
        if "mode" not in data:
            warnings.append("Missing top-level 'mode'; assuming 'build' for validation.")
        return {"mode": data.get("mode", "build"), "patch": data["patch"]}, warnings

    if {"no", "frontmatter", "content_md"} <= set(data.keys()):
        warnings.append("Input is a raw patch object; wrapping into {'mode':'build','patch':...} for validation.")
        return {"mode": "build", "patch": data}, warnings

    raise ValueError("Patch JSON must contain either {'patch': ...} or a raw {'no', 'frontmatter', 'content_md'} object.")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="JSON file to validate")
    ap.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    ap.add_argument("--schema", choices=["deck", "patch"], help="Force specific schema validation")
    args = ap.parse_args()

    content = ""
    if args.stdin:
        content = sys.stdin.read()
    elif args.file:
        p = Path(args.file).resolve()
        if not p.exists():
            print(f"Error: File not found: {p}")
            sys.exit(1)
        content = p.read_text(encoding="utf-8")
    else:
        print("Usage: python validate.py <file> OR --stdin")
        sys.exit(1)

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)

    skill_root = Path(__file__).resolve().parents[1]
    schemas_dir = skill_root / "schemas"
    deck_schema_path = schemas_dir / "deck.schema.json"
    patch_schema_path = schemas_dir / "slide_patch.schema.json"

    if not deck_schema_path.exists() or not patch_schema_path.exists():
        print("❌ Error: Schema files not found.")
        print(f"  Expected: {deck_schema_path}")
        print(f"  Expected: {patch_schema_path}")
        sys.exit(1)
    
    try:
        if args.schema == "deck" or (not args.schema and ("deck" in data or ("headmatter" in data and "slides" in data))):
            print("Validating against DeckSpec...")
            instance, warnings = _wrap_deck(data)
            validate_json(instance, deck_schema_path)
            for w in warnings:
                print(f"⚠️  {w}")
            if instance.get("mode") != "build":
                print("⚠️  Top-level 'mode' should be 'build' for strict output.")
        elif args.schema == "patch" or (not args.schema and ("patch" in data or {"no", "frontmatter", "content_md"} <= set(data.keys()))):
            print("Validating against SlidePatch...")
            instance, warnings = _wrap_patch(data)
            validate_json(instance, patch_schema_path)
            for w in warnings:
                print(f"⚠️  {w}")
            if instance.get("mode") != "build":
                print("⚠️  Top-level 'mode' should be 'build' for strict output.")
        else:
            print("Error: JSON must contain 'deck' or 'patch' root key, or specify --schema.")
            sys.exit(1)

        print("✅ Validation successful.")

    except ValidationError as e:
        print(f"❌ Validation Failed: {e.message}")
        print(f"Path: {e.json_path}")
        sys.exit(1)
    except ValueError as e:
        print(f"❌ Validation Failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
