from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import scripts.archive_sprint as arch


def test_archive_removes_todo(tmp_path):
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
    todo.write_text(
        "- [ ] [workflow/foo](issues/open/workflow/foo.md) - desc\n"
    )

    # patch constants
    arch.ROOT = repo
    arch.SPRINT_OPEN = repo / "sprints" / "open"
    arch.SPRINT_ARCHIVED = repo / "sprints" / "archived"

    arch.archive_sprint("sprint1")

    assert "workflow/foo" not in todo.read_text()
    assert (repo / "sprints/archived/sprint1").is_dir()

