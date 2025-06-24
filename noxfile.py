import nox
import nox_uv

nox.options.sessions = ["tests", "lint", "types", "api-contract"]
nox.options.default_venv_backend = "uv"


@nox_uv.session(uv_groups=["dev", "test"])
def tests(session: nox.Session) -> None:
    """Run the test suite with coverage."""
    session.run(
        "pytest",
        "--cov=econexyz",
        "--cov-report=xml",
        "--cov-report=html",
        "--cov-fail-under=80",
        external=True,
    )


@nox_uv.session(uv_only_groups=["dev"])
def lint(session: nox.Session) -> None:
    """Run linting checks."""
    session.run("ruff", "check", ".", external=True)
    session.run("ruff", "format", "--check", ".", external=True)


@nox_uv.session(uv_groups=["dev", "test"])
def types(session: nox.Session) -> None:
    """Run strict static analysis with Ty."""
    session.run("ty", "check", external=True)


@nox_uv.session(uv_groups=["test"])
def api_contract(session: nox.Session) -> None:
    """Run API contract tests."""
    session.run("pytest", "-q", "tests/api", external=True)
