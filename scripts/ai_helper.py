#!/usr/bin/env python3
"""Output current sprint plans as JSON for AI tools."""

import argparse
import json
import logging
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPRINT_DIR = ROOT / "sprints" / "current"

# Matches checklist items like:
# - [ ] [category/name](../path/to/issue.md)
# capturing the closed marker, title, and relative path.
ISSUE_PATTERN = re.compile(r"- \[( |x)\] \[([^\]]+)\]\(([^)]+)\)")
LOOSE_PATTERN = re.compile(r"-\s*\[( |x)\]\s*\[([^\]]+)\]\(([^)]+)\)")


def _format_issue(closed: bool, title: str, path: str) -> str:
    """Return a normalized checklist line for an issue."""

    mark = "x" if closed else " "
    return f"- [{mark}] [{title}]({path})"


def parse_sprint(path: Path, *, fix: bool = False) -> dict:
    """Return sprint metadata and issue list from a markdown file."""

    issues = []
    lines = path.read_text().splitlines()
    new_lines = []
    changed = False

    for idx, line in enumerate(lines, 1):
        m = ISSUE_PATTERN.search(line)
        if m:
            closed = m.group(1) == "x"
            title = m.group(2)
            rel_path = m.group(3)
            issues.append({"title": title, "path": rel_path, "closed": closed})
            formatted = _format_issue(closed, title, rel_path)
            if fix:
                new_lines.append(formatted)
                if line != formatted:
                    changed = True
            else:
                new_lines.append(line)
            continue

        if line.strip().startswith("- ["):
            lm = LOOSE_PATTERN.search(line)
            if lm:
                closed = lm.group(1) == "x"
                title = lm.group(2)
                rel_path = lm.group(3)
                issues.append({"title": title, "path": rel_path, "closed": closed})
                formatted = _format_issue(closed, title, rel_path)
                if fix:
                    new_lines.append(formatted)
                    if line != formatted:
                        changed = True
                else:
                    logging.warning(
                        "nonstandard issue format in %s:%d: %s",
                        path.name,
                        idx,
                        line.strip(),
                    )
                    new_lines.append(line)
                continue

            logging.warning(
                "unrecognized issue format in %s:%d: %s",
                path.name,
                idx,
                line.strip(),
            )
            new_lines.append(line)
        else:
            new_lines.append(line)

    if fix and changed:
        path.write_text("\n".join(new_lines) + "\n")

    return {"name": path.stem, "issues": issues}


def main() -> None:
    parser = argparse.ArgumentParser(description="Sprint helper")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="rewrite sprint files with normalized issue lines",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    plans = []
    if SPRINT_DIR.is_dir():
        for f in sorted(SPRINT_DIR.glob("*.md")):
            plans.append(parse_sprint(f, fix=args.fix))
    print(json.dumps({"sprints": plans}, indent=2))


if __name__ == "__main__":
    main()
