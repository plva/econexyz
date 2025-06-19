#!/usr/bin/env python3
"""Create a new issue file and update TODO lists."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ISSUES_DIR = ROOT / "issues" / "open"
TODO_PATH = ROOT / "TODO.md"
STATE_PATH = ROOT / "state" / "sprint.json"

CATEGORY_HEADINGS = {
    "dashboard": "## Dashboard",
    "agents": "## Agents",
    "cross": "## Cross-cutting",
    "bus": "## Event Bus",
    "workflow": "## Meta/Workflow",
}


def insert_line(path: Path, heading: str, line: str) -> None:
    """Insert a line into a markdown list under the given heading."""
    lines = path.read_text().splitlines()
    if heading not in lines:
        lines.extend(["", heading, line])
    else:
        idx = lines.index(heading) + 1
        while idx < len(lines) and not lines[idx].startswith("## "):
            idx += 1
        lines.insert(idx, line)
    path.write_text("\n".join(lines) + "\n")


def create_issue(category: str, name: str) -> None:
    today = date.today().isoformat()
    issue_path = ISSUES_DIR / category / f"{name}.md"
    issue_path.parent.mkdir(parents=True, exist_ok=True)

    content = f"""---
status: open
category: {category}
tags:
  - placeholder
created: {today}
last-updated: {today}
priority: medium
assigned: unassigned
------------------------

# {category}/{name}

TBD
"""
    issue_path.write_text(content)

    line = f"- [ ] [{category}/{name}](issues/open/{category}/{name}.md) - TBD"
    heading = CATEGORY_HEADINGS.get(category, f"## {category.title()}")
    insert_line(TODO_PATH, heading, line)

    state = json.loads(STATE_PATH.read_text())
    sprint_dir = ROOT / "sprints" / "open" / f"sprint-{state['current']}"
    sprint_meta = sprint_dir / "sprint-meta.md"
    insert_line(
        sprint_meta,
        "## Issues",
        line.replace("issues/open/", "../../issues/open/"),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="create issue")
    parser.add_argument("category", help="issue category")
    parser.add_argument("name", help="issue name (without .md)")
    args = parser.parse_args()
    create_issue(args.category, args.name)
