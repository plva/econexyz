#!/usr/bin/env python3
"""Create a new issue file and update TODO lists."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
import json
import textwrap

ROOT = Path(__file__).resolve().parents[1]
ISSUES_DIR = ROOT / "issues" / "open"
TODO_PATH = ROOT / "TODO.md"
STATE_PATH = ROOT / "state" / "sprint.json"
CONFIG_PATH = ROOT / "config" / "issue_categories.yml"

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


def render_content(category: str, name: str, tags: list[str], priority: str, today: str) -> str:
    template = textwrap.dedent(
        """
        ---
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

        # {{ category }}/{{ name }}

        TBD
        """
    )

    try:
        from jinja2 import Template
        tmpl = Template(template)
        return tmpl.render(
            category=category, name=name, tags=tags, priority=priority, today=today
        )
    except Exception:
        tag_lines = "\n".join(f"  - {t}" for t in tags)
        return textwrap.dedent(
            f"""
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

            TBD
            """
        )


def create_issue(category: str, name: str, tags: list[str] | None = None, priority: str = "medium") -> None:
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

    issue_path = ISSUES_DIR / category / f"{name}.md"
    issue_path.parent.mkdir(parents=True, exist_ok=True)

    content = render_content(category, name, tags, priority, today)
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
    parser.add_argument("--tags", help="comma-separated tags", default=None)
    parser.add_argument("--priority", default="medium", help="issue priority")
    args = parser.parse_args()
    tag_list = args.tags.split(",") if args.tags else None
    create_issue(args.category, args.name, tags=tag_list, priority=args.priority)
