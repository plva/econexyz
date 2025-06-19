from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "git_transaction.sh"


def init_repo(path: Path):
    subprocess.run(["git", "init"], cwd=path, check=True, stdout=subprocess.DEVNULL)
    (path / "base.txt").write_text("base")
    subprocess.run(["git", "add", "base.txt"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True, stdout=subprocess.DEVNULL)


def test_transaction_finalize(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    init_repo(repo)

    subprocess.run([str(SCRIPT), "start", "add file"], cwd=repo, check=True)
    (repo / "new.txt").write_text("new")
    subprocess.run([str(SCRIPT), "finalize"], cwd=repo, check=True)

    log = subprocess.check_output(["git", "log", "--pretty=%s"], cwd=repo)
    assert b"add file" in log
    assert (repo / "new.txt").exists()


def test_transaction_rollback(tmp_path):
    repo = tmp_path / "repo2"
    repo.mkdir()
    init_repo(repo)

    subprocess.run([str(SCRIPT), "start", "will rollback"], cwd=repo, check=True)
    (repo / "temp.txt").write_text("temp")
    subprocess.run([str(SCRIPT), "rollback"], cwd=repo, check=True)

    log = subprocess.check_output(["git", "log", "--pretty=%s"], cwd=repo)
    assert b"will rollback" not in log
    assert not (repo / "temp.txt").exists()
