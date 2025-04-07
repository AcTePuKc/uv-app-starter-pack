#Requires -Version 7
$ErrorActionPreference = "Stop"

# --- CONFIG ---
$VENV_DIR = ".venv"
$SCRIPT_NAME = "main.py"
$WINDOW_TITLE = "UV-App-Starter-Pack"

# Handle dry-run mode
if (-not $env:UV_APP_DRY) { $env:UV_APP_DRY = "0" }
Write-Host "Dry Run Mode: $env:UV_APP_DRY"

# --- Core Setup ---
# Check Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python not found in PATH!"
}

# Check UV
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "UV not installed. Install with: pip install uv"
}

# Create venv
if (-not (Test-Path $VENV_DIR)) {
    Write-Host "Creating venv..."
    uv venv $VENV_DIR --python python3.11
    if (-not $?) { throw "Venv creation failed!" }
}

# Activate
& "$VENV_DIR\Scripts\Activate.ps1"

# Install core requirements
Write-Host "Installing core dependencies..."
uv pip install -r requirements.txt
if (-not $?) { throw "Dependency installation failed!" }

# Conditional PyTorch install
if ($env:UV_APP_DRY -eq "0") {
    Write-Host "Installing PyTorch..."
    python install_pytorch.py
    if (-not $?) { Write-Warning "PyTorch install failed. App may lack GPU support." }
} else {
    Write-Host "[Dry Run] Skipped PyTorch installation"
}

# Launch app
Start-Process python -ArgumentList "$SCRIPT_NAME" -WindowStyle Normal -Title $WINDOW_TITLE