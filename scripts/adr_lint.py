#!/usr/bin/env python3
"""Simple ADR consistency checks."""

from __future__ import annotations

import sys
from pathlib import Path

ADR_DIR = Path("docs/adr")


def main() -> int:
    files = sorted(ADR_DIR.glob("[0-9][0-9][0-9][0-9]-*.md"))
    numbers = [int(f.name.split("-", 1)[0]) for f in files]
    ok = True

    for i, num in enumerate(numbers, start=1):
        if num != i:
            print(f"Gap or misnumbering: expected {i:04d}, found {num:04d}")
            ok = False

    index = (ADR_DIR / "index.md").read_text()
    for f in files:
        if f.name not in index:
            print(f"Missing link for {f.name} in index.md")
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
