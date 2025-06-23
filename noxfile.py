import nox

nox.options.sessions = ["tests", "lint", "types"]
nox.options.reuse_existing_virtualenvs = True


@nox.session(reuse_venv=True)
def tests(session: nox.Session) -> None:
    session.install("-e", ".[dev]")
    session.run(
        "pytest",
        "--cov=econexyz",
        "--cov-report=xml",
        "--cov-report=html",
        "--cov-fail-under=80",
    )


@nox.session
def lint(session: nox.Session) -> None:
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(reuse_venv=True)
def types(session: nox.Session) -> None:
    """Run strict static analysis with Ty."""
    session.install("-e", ".[dev]")
    session.run("ty", "check")
