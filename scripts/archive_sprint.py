#!/usr/bin/env python3
"""Archive sprint issues and metadata into per-sprint directory."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPRINT_OPEN = ROOT / "sprints" / "open"
SPRINT_ARCHIVED = ROOT / "sprints" / "archived"
ISSUE_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_issue_paths(sprint_file: Path) -> list[Path]:
    """Return list of issue file paths referenced in a sprint file."""
    issue_paths = []
    for line in sprint_file.read_text().splitlines():
        m = ISSUE_RE.search(line)
        if m and "issues/" in m.group(1):
            rel = (sprint_file.parent / m.group(1)).resolve()
            try:
                rel_path = rel.relative_to(ROOT)
            except ValueError:
                continue
            if rel_path.parts and rel_path.parts[0] == "sprints":
                rel_path = Path(*rel_path.parts[1:])
            issue_paths.append(rel_path)
    return issue_paths


def clean_empty_dirs(path: Path, stop: Path) -> None:
    """Remove empty parent directories up to stop."""
    while path != stop and path.is_dir():
        try:
            path.rmdir()
        except OSError:
            break
        path = path.parent


def archive_sprint(name: str, new: str | None = None) -> None:
    sprint_dir = SPRINT_OPEN / name
    sprint_path = sprint_dir / "sprint-meta.md"
    if not sprint_path.exists():
        raise SystemExit(f"Sprint not found: {sprint_path}")

    issue_paths = parse_issue_paths(sprint_path)

    dest_dir = SPRINT_ARCHIVED / name
    dest_open = dest_dir / "issues" / "open"
    dest_closed = dest_dir / "issues" / "closed"

    dest_open.mkdir(parents=True, exist_ok=True)
    dest_closed.mkdir(parents=True, exist_ok=True)

    # copy TODO snapshot
    shutil.copy2(ROOT / "TODO.md", dest_dir / "TODO.md")

    # remove sprint issues from top level TODO
    todo_path = ROOT / "TODO.md"
    todo_lines = []
    for line in todo_path.read_text().splitlines():
        m = ISSUE_RE.search(line)
        if m:
            rel = Path(m.group(1))
            if rel in issue_paths:
                continue
        todo_lines.append(line)
    todo_path.write_text("\n".join(todo_lines) + "\n")

    # move issues
    mapping = {}
    for rel in issue_paths:
        src = ROOT / rel
        if not src.exists():
            continue
        if rel.parts[0:2] == ("issues", "open"):
            sub = rel.relative_to("issues/open")
            dst = dest_open / sub
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), dst)
            clean_empty_dirs(src.parent, ROOT / "issues" / "open")
            mapping[str(rel)] = str(Path("issues/open") / sub)
        elif rel.parts[0:2] == ("issues", "closed"):
            sub = rel.relative_to("issues/closed")
            dst = dest_closed / sub
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), dst)
            clean_empty_dirs(src.parent, ROOT / "issues" / "closed")
            mapping[str(rel)] = str(Path("issues/closed") / sub)

    # rewrite sprint file with new paths
    lines = []
    for line in sprint_path.read_text().splitlines():
        m = ISSUE_RE.search(line)
        if m:
            old = (sprint_path.parent / m.group(1)).resolve()
            try:
                rel = old.relative_to(ROOT)
            except ValueError:
                lines.append(line)
                continue
            new_path = mapping.get(str(rel))
            if new_path:
                line = line.replace(m.group(1), new_path)
        lines.append(line)

    # move sprint file last
    dest_sprint = dest_dir / "sprint-meta.md"
    dest_sprint.write_text("\n".join(lines) + "\n")
    # remove archived sprint directory
    shutil.rmtree(sprint_dir)

    if new:
        new_dir = SPRINT_OPEN / new
        new_dir.mkdir(parents=True, exist_ok=True)
        (new_dir / "sprint-meta.md").write_text(
            f"# {new.replace('-', ' ').title()} - TBD\n\n"
            "This sprint currently has no planned issues.\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="archive sprint")
    parser.add_argument("name", help="sprint name")
    parser.add_argument(
        "--new",
        help="create a new open sprint with this name after archiving",
    )
    args = parser.parse_args()
    archive_sprint(args.name, new=args.new)


if __name__ == "__main__":
    main()
