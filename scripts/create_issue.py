#!/usr/bin/env python3
"""Create a new issue file and update TODO lists."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import json
import textwrap
from typing import Optional, List
import re

try:
    from jinja2 import Template
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False

ROOT = Path(__file__).resolve().parents[1]
ISSUES_DIR = ROOT / "issues" / "open"
TODO_PATH = ROOT / "TODO.md"
CONFIG_PATH = ROOT / "config" / "issue_categories.yml"
TEMPLATES_DIR = ROOT / "docs" / "templates"

CATEGORY_HEADINGS = {
    "dashboard": "## Dashboard",
    "agents": "## Agents",
    "cross": "## Cross-cutting",
    "bus": "## Event Bus",
    "workflow": "## Meta/Workflow",
}


def load_categories() -> dict:
    """Return category config as a dict."""
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            return {}
    return {}


def save_categories(data: dict) -> None:
    CONFIG_PATH.write_text(json.dumps(data, indent=2) + "\n")


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


def render_content(
    category: str,
    name: str,
    tags: List[str],
    priority: str,
    today: str,
    template_name: str = "default",
) -> str:
    template = textwrap.dedent(
        """\
```
------------------------
status: open
category: {{ category }}
tags:
{% for tag in tags %}
- {{ tag }}
{% endfor %}
created: {{ today }}
last-updated: {{ today }}
priority: {{ priority }}
assigned: unassigned
------------------------
```
# {{ category }}/{{ name }}
"""
    )

    body = ""
    if template_name == "bug":
        bug_path = TEMPLATES_DIR / "bug_template.md"
        if bug_path.exists():
            body = bug_path.read_text().strip()
    elif template_name == "default":
        default_path = TEMPLATES_DIR / "issue_template.md"
        if default_path.exists():
            body = default_path.read_text().strip()
    if not body:
        body = "TBD"

    template += "\n" + body

    if HAS_JINJA:
        tmpl = Template(template)
        return tmpl.render(
            category=category, name=name, tags=tags, priority=priority, today=today
        )
    else:
        tag_lines = "\n".join(f"- {t}" for t in tags)
        body_text = body
        return textwrap.dedent(f"""\
---
status: open
category: {category}
tags:
{tag_lines}
created: {today}
last-updated: {today}
priority: {priority}
assigned: unassigned
------------------------

# {category}/{name}

{body_text}
""")


def create_issue(
    category: str,
    name: str,
    tags: Optional[List[str]] = None,
    priority: str = "medium",
    template_name: str = "default",
) -> None:
    today = date.today().isoformat()
    cats = load_categories()
    if category not in cats:
        resp = input(f"Category '{category}' not found. Add it? [y/N] ")
        if resp.lower().startswith("y"):
            cats[category] = {"tags": []}
            save_categories(cats)
        else:
            raise SystemExit("Unknown category")
    if tags is None:
        tags = cats.get(category, {}).get("tags", [])
    
    # Ensure tags is always a list
    if not isinstance(tags, list):
        tags = []

    issue_path = ISSUES_DIR / category / f"{name}.md"
    issue_path.parent.mkdir(parents=True, exist_ok=True)

    content = render_content(category, name, tags, priority, today, template_name)
    issue_path.write_text(content)

    line = f"- [ ] [{category}/{name}](/issues/open/{category}/{name}.md) - TBD"
    heading = CATEGORY_HEADINGS.get(category, f"## {category.title()}")
    insert_line(TODO_PATH, heading, line)


def reopen_issue(issue: str, template_name: str = "bug") -> None:
    """Reopen a closed issue and update planning files."""
    if not issue.endswith(".md"):
        issue += ".md"
    closed_path = ROOT / "issues" / "closed" / issue
    if not closed_path.exists():
        raise SystemExit(f"Closed issue not found: {closed_path}")

    text = closed_path.read_text()
    today = date.today().isoformat()
    text = re.sub(r"^status:\s*closed", "status: open", text, flags=re.M)
    text = re.sub(r"^last-updated:.*", f"last-updated: {today}", text, flags=re.M)

    open_path = ROOT / "issues" / "open" / issue
    open_path.parent.mkdir(parents=True, exist_ok=True)
    open_path.write_text(text)

    parts = issue.split("/")
    category = parts[0]
    name = parts[-1].replace(".md", "")

    open_line = f"- [ ] [{category}/{name}](/issues/open/{category}/{name}.md)"
    closed_path = f"issues/closed/{category}/{name}.md"

    def update_planning(path: Path) -> None:
        if not path.exists():
            return
        lines = []
        for line in path.read_text().splitlines():
            if closed_path in line:
                line = line.replace(closed_path, f"issues/open/{category}/{name}.md")
                line = line.replace("- [x]", "- [ ]")
            lines.append(line)
        path.write_text("\n".join(lines) + "\n")

    update_planning(TODO_PATH)
    for meta in (ROOT / "sprints" / "open").glob("*/sprint-meta.md"):
        update_planning(meta)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="create or reopen an issue")
    parser.add_argument("category", nargs="?", help="issue category")
    parser.add_argument("name", nargs="?", help="issue name (without .md)")
    parser.add_argument("--tags", help="comma-separated tags", default=None)
    parser.add_argument("--priority", default="medium", help="issue priority")
    parser.add_argument("--template", default="default", help="issue template name")
    parser.add_argument("--reopen", help="closed issue path to reopen")
    args = parser.parse_args()

    if args.reopen:
        reopen_issue(args.reopen, template_name=args.template)
    else:
        if not args.category or not args.name:
            parser.error("category and name are required when not reopening")
        tag_list = args.tags.split(",") if args.tags else None
        create_issue(
            args.category,
            args.name,
            tags=tag_list,
            priority=args.priority,
            template_name=args.template,
        )
