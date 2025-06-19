#!/usr/bin/env python3
"""Output current sprint plans as JSON for AI tools."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPRINT_DIR = ROOT / "sprints" / "current"

# Matches checklist items like:
# - [ ] [category/name](../path/to/issue.md)
# capturing the closed marker, title, and relative path.
ISSUE_PATTERN = re.compile(r"- \[( |x)\] \[([^\]]+)\]\(([^)]+)\)")


def parse_sprint(path: Path) -> dict:
    """Return sprint metadata and issue list from a markdown file."""

    issues = []
    for line in path.read_text().splitlines():
        m = ISSUE_PATTERN.search(line)
        if m:
            closed = m.group(1) == "x"
            issues.append({
                "title": m.group(2),
                "path": m.group(3),
                "closed": closed,
            })
        elif line.strip().startswith("- ["):
            # TODO: Add dedicated validation of sprint files
            print(f"Warning: unrecognized issue format: {line}", file=sys.stderr)

    return {"name": path.stem, "issues": issues}


def main() -> None:
    plans = []
    if SPRINT_DIR.is_dir():
        for f in sorted(SPRINT_DIR.glob("*.md")):
            plans.append(parse_sprint(f))
    print(json.dumps({"sprints": plans}, indent=2))


if __name__ == "__main__":
    main()
