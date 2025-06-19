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
    (repo / "config/issue_categories.yml").write_text('{"workflow": {"tags": ["workflow"]}, "bugs": {"tags": ["bug"]}}')
    (repo / "docs/templates").mkdir(parents=True)
    (repo / "docs/templates/issue_template.md").write_text("issue body")
    (repo / "docs/templates/bug_template.md").write_text("bug body")
    ci.ROOT = repo
    ci.ISSUES_DIR = repo / "issues" / "open"
    ci.TODO_PATH = repo / "TODO.md"
    ci.STATE_PATH = repo / "state" / "sprint.json"
    ci.CONFIG_PATH = repo / "config" / "issue_categories.yml"
    ci.TEMPLATES_DIR = repo / "docs" / "templates"
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


def test_reopen_issue(tmp_path):
    repo = setup_repo(tmp_path)
    closed = repo / "issues/closed/workflow"
    closed.mkdir(parents=True)
    closed_issue = closed / "foo.md"
    closed_issue.write_text(
        "---\nstatus: closed\ncategory: workflow\ncreated: 2025-06-18\nlast-updated: 2025-06-18\npriority: medium\nassigned: none\n---\n# workflow/foo\n"
    )
    (repo / "TODO.md").write_text(
        "- [x] [workflow/foo](issues/closed/workflow/foo.md)\n"
    )
    ci.reopen_issue("workflow/foo")
    open_issue = repo / "issues/open/workflow/foo.md"
    assert open_issue.exists()
    assert "status: open" in open_issue.read_text()
    todo_text = (repo / "TODO.md").read_text()
    assert "issues/open/workflow/foo.md" in todo_text
    assert "- [ ]" in todo_text


def test_bug_template(tmp_path, monkeypatch):
    setup_repo(tmp_path)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    ci.create_issue("bugs", "login_error", template_name="bug")
    issue = tmp_path / "issues/open/bugs/login_error.md"
    assert issue.exists()
    assert "bug body" in issue.read_text()
