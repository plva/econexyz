#!/usr/bin/env bash
# Setup and activate Python virtual environment, then install requirements and run agents

set -euo pipefail

PYTHON_BIN="python3"
VENV_DIR=".venv"
REQUIREMENTS="requirements.txt"
AGENT_SCRIPT="scripts/runtime/run_agents.py"
PALETTE_SCRIPT="scripts/utils/generate_palette_css.py"
VITE_SAMPLE_DIR="dashboard/vite_sample"

# Function to print errors and exit
error_exit() {
  echo "[ERROR] $1" >&2
  exit 1
}

# Check for python3
command -v $PYTHON_BIN >/dev/null 2>&1 || error_exit "python3 is not installed. Please install Python 3.7+ and try again."

# Check for requirements.txt
if [ ! -f "$REQUIREMENTS" ]; then
  error_exit "Could not find $REQUIREMENTS in the current directory."
fi

# Check for agent script
if [ ! -f "$AGENT_SCRIPT" ]; then
  error_exit "Could not find $AGENT_SCRIPT. Are you in the project root?"
fi

# Ensure palette generation script exists
if [ ! -f "$PALETTE_SCRIPT" ]; then
  error_exit "Could not find $PALETTE_SCRIPT."
fi

# Create venv if needed
if [ ! -d "$VENV_DIR" ]; then
  echo "[INFO] Creating virtual environment in $VENV_DIR..."
  $PYTHON_BIN -m venv $VENV_DIR || error_exit "Failed to create virtual environment."
fi

# Activate venv
source $VENV_DIR/bin/activate || error_exit "Failed to activate virtual environment."
echo "[INFO] Virtual environment activated."

# Upgrade pip and install requirements
pip install --upgrade pip || error_exit "Failed to upgrade pip."
pip install -r $REQUIREMENTS || error_exit "Failed to install requirements."
echo "[INFO] Requirements installed."

# Generate dashboard color palette CSS
python "$PALETTE_SCRIPT" || error_exit "Failed to run $PALETTE_SCRIPT"

# Install and build Vite sample dashboard
if [ -d "$VITE_SAMPLE_DIR" ]; then
  command -v npm >/dev/null 2>&1 || error_exit "npm is required to build dashboard assets."
  echo "[INFO] Installing JS dependencies..."
  (cd "$VITE_SAMPLE_DIR" && npm install) || error_exit "Failed to install JS dependencies."
  echo "[INFO] Building dashboard assets..."
  (cd "$VITE_SAMPLE_DIR" && npm run build) || error_exit "Failed to build dashboard assets."
fi

# Install git hooks
if [ -x scripts/git/setup_hooks.sh ]; then
  echo "Installing git hooks..."
  ./scripts/git/setup_hooks.sh
else
  echo "Warning: scripts/git/setup_hooks.sh not found or not executable."
fi

echo "[INFO] Starting agents..."
python $AGENT_SCRIPT || error_exit "Failed to run $AGENT_SCRIPT." 
