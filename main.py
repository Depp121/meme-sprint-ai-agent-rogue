#!/usr/bin/env python3
"""Meme Sprint 3: AI Agent Goes Rogue.

The entry is one image meme, meme.png, drawn in code by draw_meme.py
(flat-cartoon robot, PIL primitives only, no stock art, no copied template).

The grader runs this program with no network, the repository read-only at
/bot, and an empty writable directory at MAKEFUN_OUTPUT_DIR (/output).
This program only copies the finished meme to /output/entry.png, so two
runs always produce the same file.

Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "meme.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SOURCE.is_file():
        print(f"missing {SOURCE}", file=sys.stderr)
        return 1
    shutil.copyfile(SOURCE, out_dir / OUTPUT_NAME)
    print(f"wrote {out_dir / OUTPUT_NAME} ({SOURCE.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
