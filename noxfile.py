import nox
import nox_uv

nox.options.sessions = ["tests", "lint", "types", "api-contract", "security"]
nox.options.default_venv_backend = "uv"


@nox_uv.session(uv_groups=["dev", "test"])
def tests(session: nox.Session) -> None:
    """Run the test suite with coverage."""
    session.run(
        "pytest",
        "--cov=econexyz",
        "--cov-report=xml",
        "--cov-report=html",
        "--cov-report=term",
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


@nox_uv.session(uv_groups=["dev"])
def api_contract(session: nox.Session) -> None:
    """Run API contract testing."""
    session.install("schemathesis")
    session.run("schemathesis", "run", "tests/api/openapi.json", external=True)


@nox_uv.session(uv_groups=["dev"])
def security(session: nox.Session) -> None:
    """Run security audit against dependencies."""
    from pathlib import Path

    # For uv.lock, we need to generate a requirements file or use uv's audit
    if Path("uv.lock").exists():
        # Use uv to generate requirements from lockfile for pip-audit
        session.run("uv", "export", "--format", "requirements.txt", "--output-file", "requirements.txt", external=True)

        # Filter out the editable install line that pip-audit can't handle
        requirements_content = Path("requirements.txt").read_text()
        filtered_lines = [line for line in requirements_content.splitlines() if not line.startswith("-e .")]
        Path("requirements.txt").write_text("\n".join(filtered_lines))

        session.run(
            "pip-audit",
            "--progress-spinner=off",
            "-r",
            "requirements.txt",
            *session.posargs,
            external=True,
        )
        # Clean up the temporary requirements file
        Path("requirements.txt").unlink(missing_ok=True)
    else:
        # Fallback to pyproject.toml if no lockfile
        session.run(
            "pip-audit",
            "--progress-spinner=off",
            "-r",
            "pyproject.toml",
            *session.posargs,
            external=True,
        )


@nox_uv.session(uv_groups=["dev", "docs"])
def docs(session: nox.Session) -> None:
    """Build the documentation."""
    session.run(
        "sphinx-build",
        "-M",
        "html",
        "docs",
        "docs/_build",
        external=True,
    )


@nox_uv.session(uv_groups=["dev"])
def secrets(session: nox.Session) -> None:
    """Run gitleaks secret scanning."""
    # Check if gitleaks is available
    try:
        session.run("gitleaks", "version", external=True, silent=True)
        # Run gitleaks scan
        session.run("gitleaks", "detect", "--verbose", "--redact", external=True)
    except Exception:
        session.log("⚠️  Gitleaks not found. Install it manually or use pre-commit hooks for secret scanning.")
        session.log("   Install with: brew install gitleaks")
        session.log("   Or download from: https://github.com/gitleaks/gitleaks/releases")
        # Don't fail the session, just warn
        return
