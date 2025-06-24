#!/usr/bin/env python3
"""Development environment health check script.

Verifies that all dev dependencies from pyproject.toml are installed and available.
"""

import sys
import tomllib
from pathlib import Path


def check_dev_dependencies():
    """Check if all dev dependencies from pyproject.toml are installed."""
    try:
        # Read pyproject.toml
        pyproject_path = Path("pyproject.toml")
        if not pyproject_path.exists():
            print("❌ pyproject.toml not found")
            return False

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        # Get dev dependencies
        dev_deps = data["project"]["optional-dependencies"]["dev"]

        # Map package names to import names for special cases
        # Some packages (like pytest-bdd and pytest-cov) have different import names than their PyPI names.
        # If you add a new dev dependency and the health check fails,
        # check if the import name differs from the package name and add it here.
        import_name_map = {
            "pytest-bdd": "pytest_bdd",
            "pytest-cov": "pytest_cov",
            "nox-uv": "nox_uv",
            "pip-audit": "pip_audit",
            "pre-commit": "pre_commit",
        }

        # Check each dependency
        missing_deps = []
        for dep in dev_deps:
            # Handle package names with extras like "pytest-bdd"
            package_name = dep.split("[")[0] if "[" in dep else dep
            import_name = import_name_map.get(package_name, package_name)

            try:
                __import__(str(import_name))
            except ImportError:
                missing_deps.append(package_name)

        if missing_deps:
            print(f"❌ Missing dev dependencies: {', '.join(missing_deps)}")
            print("💡 Run ./bootstrap.sh to install missing dependencies")
            return False

        print("✅ All dev dependencies available")
        return True

    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False


if __name__ == "__main__":
    success = check_dev_dependencies()
    sys.exit(0 if success else 1)
