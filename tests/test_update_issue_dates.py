from pathlib import Path
import subprocess
from datetime import date

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "workflow" / "update_issue_dates.py"


def init_repo(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.name", "tester"], cwd=path, check=True)
    subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=path, check=True)


def create_issue(repo: Path) -> Path:
    issue_dir = repo / "issues" / "open" / "workflow"
    issue_dir.mkdir(parents=True)
    issue = issue_dir / "foo.md"
    issue.write_text(
        "---\n"
        "status: open\n"
        "category: workflow\n"
        "created: 2025-06-18\n"
        "last-updated: 2025-06-18\n"
        "priority: medium\n"
        "assigned: unassigned\n"
        "---\n"
        "# workflow/foo\n"
    )
    return issue


def test_update_issue_dates(tmp_path):
    repo = tmp_path
    init_repo(repo)
    issue = create_issue(repo)
    subprocess.run(["git", "add", str(issue)], cwd=repo, check=True)
    subprocess.run(["python", str(SCRIPT)], cwd=repo, check=True)
    text = issue.read_text()
    assert f"last-updated: {date.today().isoformat()}" in text
