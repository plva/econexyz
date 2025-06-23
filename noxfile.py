import nox

nox.options.sessions = ["tests", "lint"]
nox.options.reuse_existing_virtualenvs = True


@nox.session(reuse_venv=True)
def tests(session: nox.Session) -> None:
    session.install("-e", ".[dev]")
    session.run("pytest", "-q")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")
