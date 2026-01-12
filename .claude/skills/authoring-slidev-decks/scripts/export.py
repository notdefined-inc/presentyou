#!/usr/bin/env python3
"""
Wrapper for slidev export.
"""
import argparse
import subprocess
import sys
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", "-p", required=True, help="Path to Slidev project directory")
    ap.add_argument("--format", choices=["pptx", "pdf", "png", "md"], default="pptx")
    ap.add_argument("--output", help="Output file path (default: exports/deck-export.<format>)")
    args = ap.parse_args()

    project_root = Path(args.project).resolve()
    if not (project_root / "package.json").exists():
        print(f"❌ Error: Not a Slidev project (missing package.json): {project_root}")
        sys.exit(1)

    print(f"Exporting to {args.format}...")
    
    output = args.output or f"exports/deck-export.{args.format}"
    (project_root / Path(output).parent).mkdir(parents=True, exist_ok=True)

    cmd = ["npx", "--no-install", "slidev", "export", "--format", args.format, "--output", output]
    
    try:
        subprocess.run(cmd, cwd=project_root, check=True)
        print(f"✅ Exported to {output}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
