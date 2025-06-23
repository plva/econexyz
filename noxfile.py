import nox

nox.options.sessions = ["tests", "lint", "types"]
nox.options.reuse_existing_virtualenvs = True


@nox.session
def tests(session: nox.Session) -> None:
    session.install(".[test]")
    session.run("pytest", "-q", "--cov")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(reuse_venv=True)
def types(session: nox.Session) -> None:
    """Run strict static analysis with Ty."""
    session.install("ty")
    session.run("ty", "--strict")
