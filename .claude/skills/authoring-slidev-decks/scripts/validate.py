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

def validate_json(data: dict, schema_path: Path) -> None:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validate(instance=data, schema=schema)

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
        print("Usage: python tools/validate.py <file> OR --stdin")
        sys.exit(1)

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)

    root = Path(__file__).resolve().parents[1]
    
    try:
        if args.schema == "deck" or (not args.schema and "deck" in data):
            print("Validating against DeckSpec...")
            validate_json(data, root / "llm/schema/deck.schema.json")
            if data.get("mode") != "build":
                 print("Warning: 'mode' should be 'build' for strict output.")
        elif args.schema == "patch" or (not args.schema and "patch" in data):
            print("Validating against SlidePatch...")
            validate_json(data, root / "llm/schema/slide_patch.schema.json")
            if data.get("mode") != "build":
                 print("Warning: 'mode' should be 'build' for strict output.")
        else:
            print("Error: JSON must contain 'deck' or 'patch' root key, or specify --schema.")
            sys.exit(1)

        print("✅ Validation successful.")

    except ValidationError as e:
        print(f"❌ Validation Failed: {e.message}")
        print(f"Path: {e.json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
