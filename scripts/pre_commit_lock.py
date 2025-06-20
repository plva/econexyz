#!/usr/bin/env python3
"""Pre-commit hook to warn about edits to locked files."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def parse_lock(lock_path: Path) -> dict[str, str]:
    data = {}
    for line in lock_path.read_text().splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"')
    return data


def get_staged_files(repo_root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def main() -> None:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    )
    repo_root = Path(result.stdout.strip()) if result.returncode == 0 else Path.cwd()
    locks_dir = repo_root / "locks"

    staged_files = get_staged_files(repo_root)

    user = subprocess.run(
        ["git", "config", "user.name"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    ).stdout.strip() or os.getenv("USER", "")

    warnings = []

    if locks_dir.exists():
        for lock_file in locks_dir.glob("*.lock"):
            lock_data = parse_lock(lock_file)
            locked_file = lock_data.get("file")
            lock_user = lock_data.get("user")
            ts = lock_data.get("timestamp", "")
            reason = lock_data.get("reason", "")
            if (
                locked_file
                and locked_file in staged_files
                and lock_user
                and lock_user != user
            ):
                warnings.append(
                    f"\u26A0\uFE0F Warning: You're modifying '{locked_file}', "
                    f"currently locked by user '{lock_user}' since '{ts}'.\n"
                    f"Reason: {reason}"
                )

    if warnings:
        print("\n".join(warnings))
    sys.exit(0)


if __name__ == "__main__":
    main()
