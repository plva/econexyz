#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: ./bootstrap.sh [ARGS...]

Bootstraps the project using a local Python virtual environment.
Additional arguments are executed within the environment.

  --yes-hooks   install git pre-commit hooks without prompting
  --no-hooks    skip git pre-commit hook installation
USAGE
}


# Parse arguments for hook installation flags
install_hooks=""
args=()
for arg in "$@"; do
  case "$arg" in
    --yes-hooks) install_hooks="yes" ;;
    --no-hooks) install_hooks="no" ;;
    --help)
      usage
      exit 0
      ;;
    *) args+=("$arg") ;;
  esac
done

# Only set args if the array is not empty
if [ ${#args[@]} -gt 0 ]; then
  set -- "${args[@]}"
else
  set --
fi

# Ensure we are in the repo root
cd "$(dirname "$0")"

# Install uv if missing
if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Install just if missing
if ! command -v just >/dev/null 2>&1; then
  echo "Installing just..."
  uv tool install rust-just
fi

# Create or reuse virtual environment
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

# Always activate environment (even if already activated, this is safe)
# This ensures the venv is active even if the user has exited it
source .venv/bin/activate

# Install dependencies if lock file exists
if [ -f uv.lock ]; then
  uv pip install -r uv.lock
elif [ -f pyproject.toml ]; then
  uv pip install -e .[dev,test]
fi

# Optionally install pre-commit hooks
if [ -z "$install_hooks" ]; then
  read -r -p "Install git pre-commit hooks? [y/N] " reply
  if [[ $reply =~ ^[Yy] ]]; then
    install_hooks="yes"
  else
    install_hooks="no"
  fi
fi

if [ "$install_hooks" = "yes" ]; then
  if ! command -v pre-commit >/dev/null 2>&1; then
    uv pip install pre-commit
  fi
  pre-commit install --install-hooks >/dev/null 2>&1 || true
fi

# Forward arguments to the given command if provided
if [ "$#" -gt 0 ]; then
  "$@"
else
  usage
fi
