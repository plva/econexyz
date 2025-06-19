from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import scripts.create_issue as ci


def setup_repo(tmp_path: Path):
    repo = tmp_path
    (repo / "issues/open").mkdir(parents=True)
    (repo / "sprints/open/sprint-1").mkdir(parents=True)
    (repo / "sprints/open/sprint-1/sprint-meta.md").write_text("# Sprint\n\n## Issues\n")
    (repo / "state").mkdir()
    (repo / "state/sprint.json").write_text('{"current": 1}')
    (repo / "TODO.md").write_text("")
    (repo / "config").mkdir()
    (repo / "config/issue_categories.yml").write_text('{"workflow": {"tags": ["workflow"]}}')
    ci.ROOT = repo
    ci.ISSUES_DIR = repo / "issues" / "open"
    ci.TODO_PATH = repo / "TODO.md"
    ci.STATE_PATH = repo / "state" / "sprint.json"
    ci.CONFIG_PATH = repo / "config" / "issue_categories.yml"
    return repo


def test_create_issue_basic(tmp_path, monkeypatch):
    setup_repo(tmp_path)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    ci.create_issue("workflow", "foo", priority="low")
    issue = tmp_path / "issues/open/workflow/foo.md"
    assert issue.exists()
    text = issue.read_text()
    assert "priority: low" in text
    todo = (tmp_path / "TODO.md").read_text()
    assert "workflow/foo" in todo


def test_create_issue_new_category(tmp_path, monkeypatch):
    setup_repo(tmp_path)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    ci.create_issue("newcat", "bar")
    config = ci.CONFIG_PATH.read_text()
    assert "newcat" in config
