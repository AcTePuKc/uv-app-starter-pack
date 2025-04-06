# PowerShell launcher for UV-App-Starter-Pack
# Set environment variable $env:UV_APP_DRY=1 to skip torch install
# Example: $env:UV_APP_DRY=1; .\run_uv.ps1
# Defaulting to install torch if not set

param(
    [string]$PythonVersion = "python3.11",
    [string]$VenvDir = ".venv",
    [string]$ScriptName = "main.py",
    [string]$WindowTitle = "UV-App-Starter-Pack"
)

# Stop script on first error
$ErrorActionPreference = 'Stop'

# Check Python (Try specific, fallback to generic)
$PythonExePath = Get-Command $PythonVersion -ErrorAction SilentlyContinue
if (-not $PythonExePath) {
    Write-Warning "Specific Python $PythonVersion not found, checking for generic 'python'..."
    $PythonExePath = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonExePath) {
        Write-Error "Python ($PythonVersion or python) is not installed or not in PATH!"
        pause
        exit 1
    }
    Write-Host "Found generic python at $($PythonExePath.Source)"
    $PythonVersion = "python" # Use generic for venv creation if specific wasn't found
} else {
    Write-Host "Found $PythonVersion at $($PythonExePath.Source)"
}


# Check uv
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Error "uv is not installed. Run: pip install uv"
    pause
    exit 1
}

# Determine full path for venv
$FullVenvDir = Join-Path -Path $PSScriptRoot -ChildPath $VenvDir

# Create virtual environment if pyvenv.cfg doesn't exist
if (-not (Test-Path (Join-Path $FullVenvDir "pyvenv.cfg"))) {
    Write-Host "Creating venv..."
    # Use the Python version found earlier
    uv venv $FullVenvDir --python $PythonVersion
} else {
    Write-Host "Venv exists."
}


# Determine Python executable within venv
$VenvPython = Join-Path -Path $FullVenvDir -ChildPath "Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Error "Could not find python.exe in $FullVenvDir\Scripts"
    pause
    exit 1
}


# Activate environment (Still needed for multiple commands if not using 'uv run')
# Note: Activation in PS might not reliably affect external processes started later like Start-Process
# It's generally better to call the venv python directly.
. (Join-Path $FullVenvDir 'Scripts\Activate.ps1')


# Show Python version
Write-Host "Using Python from venv:"
& $VenvPython -c "import sys; print(sys.executable); print(sys.version.split()[0])"

# Sync base deps
Write-Host "Syncing base requirements..."
uv pip sync requirements.txt # uv should pick up the activated venv


# Install correct PyTorch
Write-Host "Checking PyTorch installation..."
$TorchArgs = @()
# Check environment variable UV_APP_DRY
if ($env:UV_APP_DRY -eq "1") {
    Write-Host "Dry run enabled for PyTorch (UV_APP_DRY=1)."
    $TorchArgs += "--dry"
}
# Run install_torch.py using the venv python
& $VenvPython install_torch.py $TorchArgs


# Launch the app in a new PowerShell window with title
Write-Host "Setup complete! Launching the app..."
Start-Process powershell -WindowStyle Normal -WorkingDirectory $PSScriptRoot -ArgumentList @(
    "-NoExit", # Keeps window open after script finishes (remove if not desired)
    "-Command",
    # Ensure the command uses the specific venv python
    "`$host.ui.RawUI.WindowTitle = '$WindowTitle'; & '$VenvPython' '$ScriptName'"
)

Write-Host "Launched $ScriptName in a new PowerShell window titled '$WindowTitle'"

# Reset error action preference if needed
# $ErrorActionPreference = 'Continue'