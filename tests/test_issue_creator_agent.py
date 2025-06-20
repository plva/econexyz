from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from econexyz.agents.issue_creator import SmartIssueCreatorAgent
from econexyz.message_bus.in_memory import InMemoryMessageBus
from econexyz.storage.sqlite_store import SQLiteKnowledgeStore
import scripts.workflow.create_issue as ci


def setup_repo(tmp_path: Path):
    (tmp_path / "issues/open").mkdir(parents=True)
    (tmp_path / "config").mkdir()
    (tmp_path / "docs/templates").mkdir(parents=True)
    (tmp_path / "docs/templates/issue_template.md").write_text("body")
    (tmp_path / "TODO.md").write_text("")
    config = '{"workflow": {"tags": ["workflow"]}, "bugs": {"tags": ["bug"]}}'
    (tmp_path / "config/issue_categories.yml").write_text(config)

    ci.ROOT = tmp_path
    ci.ISSUES_DIR = tmp_path / "issues" / "open"
    ci.TODO_PATH = tmp_path / "TODO.md"
    ci.CONFIG_PATH = tmp_path / "config" / "issue_categories.yml"
    ci.TEMPLATES_DIR = tmp_path / "docs" / "templates"


def test_choose_category():
    bus = InMemoryMessageBus()
    store = SQLiteKnowledgeStore(":memory:")
    agent = SmartIssueCreatorAgent("tester", bus, store)
    assert agent._choose_category("Fix bug in login") == "bugs"
    assert agent._choose_category("Update dashboard colors") == "dashboard"


def test_handle_request_creates_issue(tmp_path, monkeypatch):
    setup_repo(tmp_path)
    bus = InMemoryMessageBus()
    db = tmp_path / "store.db"
    store = SQLiteKnowledgeStore(str(db))
    monkeypatch.setattr("builtins.input", lambda _: "y")
    agent = SmartIssueCreatorAgent("creator", bus, store, config_path=ci.CONFIG_PATH)
    bus.publish("issue_request", {"description": "fix login bug", "priority": "low"})
    issue_file = tmp_path / "issues/open/bugs/fix_login_bug.md"
    assert issue_file.exists()
    text = issue_file.read_text()
    assert "priority: low" in text
