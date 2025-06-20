from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.runtime.ai_helper import parse_sprint, _format_issue


def test_parse_and_fix(tmp_path):
    sprint = tmp_path / "sprint.md"
    sprint.write_text(
        "# Sprint\n\n## Issues\n- [ ] [cat/foo](../issues/open/cat/foo.md)\n- [x][cat/bar](../issues/closed/cat/bar.md) \n- [ ] bad line\n"
    )
    plan = parse_sprint(sprint)
    assert plan["name"] == "sprint"
    # Nonstandard line still parsed but triggers warning
    assert len(plan["issues"]) == 2

    parse_sprint(sprint, fix=True)
    plan = parse_sprint(sprint)
    lines = sprint.read_text().splitlines()
    assert len(plan["issues"]) == 2
    assert lines[3] == _format_issue(False, "cat/foo", "../issues/open/cat/foo.md")
    assert lines[4] == _format_issue(True, "cat/bar", "../issues/closed/cat/bar.md")


def test_bug_summary(tmp_path):
    sprint = tmp_path / "sprint.md"
    sprint.write_text(
        "# Sprint\n\n## Issues\n- [ ] [cat/foo](../issues/open/cat/foo.md)\n\n## Bug Summary\nCritical: 1\nHigh: 2\nRegressions: 1\n"
    )
    plan = parse_sprint(sprint)
    assert plan["bugs"]["critical"] == 1
    assert plan["bugs"]["high"] == 2
    assert plan["bugs"]["regressions"] == 1

