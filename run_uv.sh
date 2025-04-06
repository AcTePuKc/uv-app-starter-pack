#!/bin/bash
set -e # Exit immediately if a command exits with a non-zero status.

# --- Config ---
# Set UV_APP_DRY=1 externally to skip torch install
# Example: export UV_APP_DRY=1; ./run_uv.sh
# Defaulting to install torch if not set
: "${UV_APP_DRY:=0}" # Sets UV_APP_DRY to 0 if it's not already set

VENV_DIR=".venv"
PYTHON_TO_USE="python3.11"
SCRIPT_NAME="main.py"
# --- End Config ---


# Check Python (Try specific, fallback to generic)
if ! command -v "$PYTHON_TO_USE" &> /dev/null; then
    echo "Specific Python $PYTHON_TO_USE not found, checking for generic python..."
    if ! command -v python &> /dev/null; then
        echo "Python ($PYTHON_TO_USE or python) is not installed or not in PATH!"
        exit 1
    fi
     echo "Found generic python, will attempt to use it."
     PYTHON_TO_USE="python"
else
    echo "Found $PYTHON_TO_USE."
fi


# Check uv
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Install it with: pip install uv"
    exit 1
fi

# Create virtual environment (edit python version as needed)
if [ ! -f "$VENV_DIR/pyvenv.cfg" ]; then
    echo "Creating venv..."
    uv venv "$VENV_DIR" --python "$PYTHON_TO_USE"
else
    echo "Venv exists."
fi

# Define Python executable in venv
VENV_PYTHON="$VENV_DIR/bin/python"

# Activate environment (Still needed for multiple commands if not using 'uv run')
source "$VENV_DIR/bin/activate"

# Show Python version
echo "Using Python from venv:"
"$VENV_PYTHON" -c "import sys; print(sys.executable); print(sys.version.split()[0])"

# Sync dependencies
echo "Syncing base requirements..."
uv pip sync requirements.txt # uv should use activated venv

# Install correct PyTorch
echo "Checking PyTorch installation..."
TORCH_ARGS=""
if [ "$UV_APP_DRY" = "1" ]; then
    echo "Dry run enabled for PyTorch (UV_APP_DRY=1)."
    TORCH_ARGS="--dry"
fi
# Run install_torch.py using the venv python
"$VENV_PYTHON" install_torch.py $TORCH_ARGS

# Launch the app
echo "Setup complete! Launching the app..."
"$VENV_PYTHON" "$SCRIPT_NAME"

echo "Application finished."