
# 📦 UV-App-Starter-Pack

A clean, cross-platform Python GUI app bootstrapper using **PySide6** and **uv**. This starter pack helps you set up apps that require flexible environment handling (like Torch/CUDA), with minimal effort.

---
## Prerequisites

*   **Python:** A compatible version (defaults to `3.11` in launchers, but can be changed). Ensure it's in your system's PATH.
*   **uv:** The Python package manager. Install it if you haven't already:
    ```bash
    pip install uv
    # or pipx install uv
    ```
    See the [official uv documentation](https://github.com/astral-sh/uv#installation) for more ways to install.
    
## 🧰 Features

- Python `3.11` virtual environment with `uv`
- Optional PyTorch installation (auto-matches CUDA version)
- Supports `--dry` or `UV_APP_DRY=1` to skip PyTorch install (good for testing)
- Cross-platform launchers: `.bat`, `.ps1`, `.sh`
- Clean GUI stub using `PySide6` (can be replaced with your own GUI)
- Friendly for beginners and pro devs alike

---

### 🛠 Folder Contents

| File                  | Purpose |
|-----------------------|---------|
| `main.py`             | Launches your GUI app |
| `gui/gui_app.py`      | PySide6 GUI logic (`UVAppWindow`) |
| `gui/__init__.py`     | Makes `gui` a Python package |
| `install_torch.py`  | Smart PyTorch installer (CUDA-aware) |
| `requirements.txt`    | Base dependencies (synced by `uv`) |
| `run_uv.bat`          | Windows launcher |
| `run_uv.ps1`          | PowerShell launcher |
| `run_uv.sh`           | Linux/macOS/WSL launcher |

---

### 🚀 Quickstart

<details>
<summary><strong>🪟 Windows (run_uv.bat)</strong></summary>

```bat
:: Optional: Skip torch install (for testing)
set UV_APP_DRY=1

:: Run this script
run_uv.bat
```

</details>

<details>
<summary><strong>💻 PowerShell (run_uv.ps1)</strong></summary>

```powershell
$env:UV_APP_DRY=1   # Optional
./run_uv.ps1
```

</details>

<details>
<summary><strong>🐧 Linux/macOS (run_uv.sh)</strong></summary>

```bash
export UV_APP_DRY=1   # Optional
chmod +x run_uv.sh
./run_uv.sh
```

</details>

---

### ⚙️ Environment Behavior

| Variable / Flag     | Effect |
|---------------------|--------|
| `UV_APP_DRY=1`      | Skips PyTorch installation |
| `--dry`             | Same effect when passed directly to `install_pytorch.py` |
| Python version      | Controlled inside the launcher (`python3.11` by default) |

---

### 🧪 Testing (No CUDA/No Torch)

If you're just testing the GUI, set `UV_APP_DRY=1` in your script or terminal. This skips the heavy install step.

---

### 🧠 Ideas for Expansion

- Add translation files or multi-language GUI switching
- Drop in custom GUI logic (e.g. Whisper, TTS, transcription)
- Add `.env` support for dynamic configuration

---
