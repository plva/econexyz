#!/usr/bin/env python3
"""Update last-updated fields for staged issue files."""
from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path
import re


def get_repo_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
    )
    return Path(result.stdout.strip()) if result.returncode == 0 else Path.cwd()


def get_staged_files(repo: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    )
    files = [repo / f for f in result.stdout.splitlines() if f.startswith("issues/") and f.endswith(".md")]
    return files


def update_file(path: Path, today: str) -> bool:
    text = path.read_text()
    if "last-updated:" not in text:
        return False
    new_text = re.sub(r"^last-updated:.*", f"last-updated: {today}", text, flags=re.MULTILINE)
    if new_text != text:
        path.write_text(new_text)
        return True
    return False


def main() -> None:
    repo = get_repo_root()
    files = get_staged_files(repo)
    if not files:
        return
    today = date.today().isoformat()
    updated = False
    for f in files:
        if f.exists() and update_file(f, today):
            updated = True
            subprocess.run(["git", "add", str(f)], cwd=repo, check=False)
    if updated:
        print("updated issue last-updated fields")


if __name__ == "__main__":
    main()
