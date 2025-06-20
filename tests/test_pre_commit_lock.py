from pathlib import Path
import os
import subprocess

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "pre_commit_lock.py"


def test_pre_commit_warns_on_locked_file(tmp_path, monkeypatch):
    # initialize git repo
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "tester"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "tester@example.com"], cwd=tmp_path, check=True)

    # create file and commit
    todo = tmp_path / "TODO.md"
    todo.write_text("initial")
    subprocess.run(["git", "add", "TODO.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=tmp_path, check=True)

    # create lock by another user
    locks = tmp_path / "locks"
    locks.mkdir()
    lock_file = locks / "todo.lock"
    lock_file.write_text(
        "user: \"someone\"\n"
        "timestamp: \"2025-06-21T00:00:00Z\"\n"
        "reason: \"testing\"\n"
        "file: \"TODO.md\"\n"
    )

    # modify and stage file
    todo.write_text("change")
    subprocess.run(["git", "add", "TODO.md"], cwd=tmp_path, check=True)

    env = os.environ.copy()
    env["USER"] = "tester"
    result = subprocess.run([str(SCRIPT)], cwd=tmp_path, capture_output=True, text=True, env=env)

    assert "currently locked" in result.stdout
