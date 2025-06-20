"""Example showing how to use git_transaction.sh."""

from pathlib import Path
import subprocess

SCRIPT = Path(__file__).resolve().parent / "git_transaction.sh"


def main():
    subprocess.run([str(SCRIPT), "start", "Add example file"], check=True)
    Path("example.txt").write_text("example\n")
    subprocess.run([str(SCRIPT), "finalize"], check=True)


if __name__ == "__main__":
    main()
