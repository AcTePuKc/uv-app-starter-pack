#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# --- Config ---
# Set UV_APP_DRY=1 externally to skip torch install
# Example: export UV_APP_DRY=1; ./run_uv.sh

# --- CONFIG ---
VENV_DIR=".venv"
SCRIPT_NAME="main.py"
WINDOW_TITLE="UV-App-Starter-Pack"

# Handle dry-run mode
UV_APP_DRY=${UV_APP_DRY:-0}
echo "Dry Run Mode: $UV_APP_DRY"

# --- Core Setup ---
# Check Python
if ! command -v python3.11 &> /dev/null; then
    echo "ERROR: Python 3.11 not found!"
    exit 1
fi

# Check UV
if ! command -v uv &> /dev/null; then
    echo "ERROR: uv not installed. Install with: pip install uv"
    exit 1
fi

# Create venv
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating venv..."
    uv venv "$VENV_DIR" --python python3.11 || { echo "Venv creation failed!"; exit 1; }
fi

# Activate
source "$VENV_DIR/bin/activate"

# Install core requirements
echo "Installing core dependencies..."
uv pip install -r requirements.txt || { echo "Dependency installation failed!"; exit 1; }

# Conditional PyTorch install
if [ "$UV_APP_DRY" = "0" ]; then
    echo "Installing PyTorch..."
    python install_pytorch.py || echo "WARNING: PyTorch install failed. App may lack GPU support."
else
    echo "[Dry Run] Skipped PyTorch installation"
fi

# Launch app
echo "Starting application..."
python "$SCRIPT_NAME"