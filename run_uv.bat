@echo off
setlocal enabledelayedexpansion

:: ---------------- CONFIG ----------------
:: Set UV_APP_DRY=1 externally or here to skip torch install
:: Example: set UV_APP_DRY=1
:: Defaulting to 0 (install torch) if not set
if not defined UV_APP_DRY (
  set UV_APP_DRY=0
)

set VENV_DIR=.venv
set PYTHON_TO_USE=python3.11
set SCRIPT_NAME=main.py
set WINDOW_TITLE=UV-App-Starter-Pack
:: ----------------------------------------

:: Check for Python (find specific version if possible, fallback)
where %PYTHON_TO_USE% >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
  echo Specific Python %PYTHON_TO_USE% not found, checking for generic python...
  where python >nul 2>nul || (
    echo Python (%PYTHON_TO_USE% or python) is not installed or not in PATH!
    pause
    exit /b 1
  )
  echo Found generic python, will attempt to use it.
  set PYTHON_TO_USE=python
) else (
   echo Found %PYTHON_TO_USE%.
)


:: Check for uv
where uv >nul 2>nul || (
    echo uv is not installed. Install it with: pip install uv
    pause
    exit /b 1
)

:: -------------------------------------
:: Creating a virtual environment
:: -------------------------------------
if not exist "%VENV_DIR%\pyvenv.cfg" (
    echo Creating venv...
    uv venv %VENV_DIR% --python %PYTHON_TO_USE% || (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
   echo Venv exists.
)

set PYTHON_EXE=%VENV_DIR%\Scripts\python.exe

:: Activate environment (Still needed for multiple commands if not using 'uv run')
call %VENV_DIR%\Scripts\activate

:: Print Python version (optional)
echo Using Python from venv:
%PYTHON_EXE% -c "import sys; print(sys.executable); print(sys.version.split()[0])"

:: Sync base dependencies (excluding torch)
echo Syncing base requirements...
uv pip sync requirements.txt || (
    echo Failed to sync requirements.
    pause
    exit /b 1
)

:: Install correct PyTorch for current CUDA version
echo Checking PyTorch installation...
set TORCH_ARGS=
if "%UV_APP_DRY%"=="1" (
    echo Dry run enabled for PyTorch.
    set TORCH_ARGS=--dry
)
REM Run install_torch.py using the venv python
%PYTHON_EXE% install_torch.py %TORCH_ARGS% || (
    echo PyTorch installation script failed.
    pause
    exit /b 1
)


:: ---------------- RUN GUI ----------------
echo.
echo Setup complete! Launching the app...

REM Using start still launches a new window, which might be desired.
REM Use the python executable from the venv directly.
start "%WINDOW_TITLE%" "%PYTHON_EXE%" "%SCRIPT_NAME%"

:: Simple check if start succeeded (may not catch Python errors)
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to start the application process.
    pause
)

endlocal