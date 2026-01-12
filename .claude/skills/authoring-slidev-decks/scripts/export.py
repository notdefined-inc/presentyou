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
    ap.add_argument("--format", choices=["pptx", "pdf", "png", "md"], default="pptx")
    args = ap.parse_args()

    print(f"Exporting to {args.format}...")
    
    cmd = ["npx", "slidev", "export", "--format", args.format, "--output", f"exports/deck-export.{args.format}"]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Exported to exports/deck-export.{args.format}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
