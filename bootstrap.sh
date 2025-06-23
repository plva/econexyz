#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: ./bootstrap.sh [ARGS...]

Bootstraps the project using a local Python virtual environment.
Additional arguments are executed within the environment.

  --yes-hooks   install git pre-commit hooks without prompting
  --no-hooks    skip git pre-commit hook installation

Examples:
  ./bootstrap.sh              # Setup and show usage
  ./bootstrap.sh test         # Setup and run 'test' command
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

echo "Activating virtual environment..."
# Always activate environment (even if already activated, this is safe)
# This ensures the venv is active even if the user has exited it
source .venv/bin/activate

# Install dependencies
if [ -f uv.lock ]; then
  uv pip install -r uv.lock
fi

# Always install dev dependencies for development
if [ -f pyproject.toml ]; then
  uv pip install -e ".[dev]"
  uv pip install pytest-bdd pytest-cov
fi

# Install Commitizen for commit management
  uv tool install commitizen
  uv tool upgrade commitizen || true

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
  echo "Installed git pre-commit hooks"
fi

# Forward arguments to the given command if provided
if [ "$#" -gt 0 ]; then
  "$@"
else
  echo ""
  echo "✅ Bootstrap complete! Virtual environment is ready."
  echo ""
  echo "To enter the virtual environment, run:"
  echo -e "  \033[1;32msource .venv/bin/activate\033[0m"
  echo ""
  echo "Then you can use commands like:"
  echo -e "  \033[1;36mjust test\033[0m    # Run tests"
  echo -e "  \033[1;36mjust lint\033[0m    # Check code style"
fi
