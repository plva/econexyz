from pathlib import Path
import os
import subprocess

CREATE_LOCK = Path(__file__).resolve().parents[1] / "scripts" / "utils" / "create_lock.sh"


def test_create_lock(tmp_path, monkeypatch):
    env = os.environ.copy()
    env["USER"] = "tester"
    subprocess.run([str(CREATE_LOCK), "sample", "data/file.txt", "for test"], cwd=tmp_path, check=True, env=env)
    lock_file = tmp_path / "locks" / "sample.lock"
    assert lock_file.exists()
    content = lock_file.read_text()
    assert "user:" in content
    assert "timestamp:" in content
    assert 'reason: "for test"' in content
    assert 'file: "data/file.txt"' in content
