@echo off
setlocal enabledelayedexpansion

:: --- CONFIG ---
set VENV_DIR=.venv
set SCRIPT_NAME=main.py
set WINDOW_TITLE=UV-App-Starter-Pack

if not defined UV_APP_DRY set "UV_APP_DRY=0"
echo Dry Run Mode: %UV_APP_DRY%

:: --- Core Setup ---
where python >nul || (echo ERROR: Python missing! && pause && exit /b 1)
where uv >nul || (echo ERROR: UV missing! && pause && exit /b 1)

if not exist "%VENV_DIR%" (
    echo Creating venv...
    uv venv "%VENV_DIR%" --python python3.11 || (
        echo ERROR: Venv creation failed!
        pause
        exit /b 1
    )
)

call "%VENV_DIR%\Scripts\activate"

:: Install core requirements
echo Installing core dependencies...
uv pip install -r requirements.txt || (
    echo ERROR: Dependency installation failed!
    pause
    exit /b 1
)

:: Conditional PyTorch install
if "%UV_APP_DRY%"=="0" (
    echo Installing PyTorch...
    python install_torch.py || (
        echo WARNING: PyTorch install failed. App may lack GPU support.
    )
) else (
    echo [Dry Run] Skipped PyTorch installation
)

start "%WINDOW_TITLE%" cmd /k ""%VENV_DIR%\Scripts\python.exe" "%SCRIPT_NAME%""