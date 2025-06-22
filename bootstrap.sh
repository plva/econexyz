#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: ./bootstrap.sh [ARGS...]

Bootstraps the project using a local Python virtual environment.
Additional arguments are executed within the environment.
USAGE
}

if [[ ${1-} == "--help" ]]; then
  usage
  exit 0
fi

# Ensure we are in the repo root
cd "$(dirname "$0")"

# Install uv if missing
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create or reuse virtual environment
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# Activate environment
source .venv/bin/activate

# Install dependencies if lock file exists
if [ -f uv.lock ]; then
  uv pip install -r uv.lock
elif [ -f pyproject.toml ]; then
  uv pip install -e .
fi

# Install pre-commit hooks if available
if ! command -v pre-commit >/dev/null 2>&1; then
  uv pip install pre-commit
fi
pre-commit install --install-hooks >/dev/null 2>&1 || true

# Forward arguments to the given command if provided
if [ "$#" -gt 0 ]; then
  "$@"
else
  usage
fi
