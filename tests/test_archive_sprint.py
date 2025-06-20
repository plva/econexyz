from pathlib import Path
import subprocess
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import scripts.workflow.archive_sprint as arch


def setup_repo(tmp_path: Path, done: bool) -> tuple[Path, Path]:
    repo = tmp_path
    (repo / "issues/open/workflow").mkdir(parents=True)
    (repo / "issues/open/workflow/foo.md").write_text("issue")

    sprint_dir = repo / "sprints/open/sprint1"
    sprint_dir.mkdir(parents=True)
    sprint_meta = sprint_dir / "sprint-meta.md"
    sprint_meta.write_text(
        "# Sprint\n\n## Issues\n- [ ] [workflow/foo](../../issues/open/workflow/foo.md)\n"
    )

    todo = repo / "TODO.md"
    check = "x" if done else " "
    todo.write_text(
        f"- [{check}] [workflow/foo](issues/open/workflow/foo.md) - desc\n"
    )

    arch.ROOT = repo
    arch.SPRINT_OPEN = repo / "sprints" / "open"
    arch.SPRINT_ARCHIVED = repo / "sprints" / "archived"
    return repo, todo


def test_archive_removes_completed_todo(tmp_path):
    repo, todo = setup_repo(tmp_path, done=True)
    arch.archive_sprint("sprint1")
    assert "workflow/foo" not in todo.read_text()
    assert (repo / "sprints/archived/sprint1").is_dir()


def test_archive_keeps_open_todo(tmp_path):
    repo, todo = setup_repo(tmp_path, done=False)
    arch.archive_sprint("sprint1")
    text = todo.read_text()
    assert "workflow/foo" in text
    assert "- [ ]" in text
