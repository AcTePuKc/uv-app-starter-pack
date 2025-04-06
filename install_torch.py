# install_torch_uv.py
# ---------------------
# Smart installer for PyTorch based on CUDA version.
# Use --dry or set UV_APP_DRY=1 to skip actual install (for testing or CI).
# ---------------------

import subprocess
import sys
import os

def detect_cuda_version():
    try:
        output = subprocess.check_output(["nvcc", "--version"], text=True)
        for line in output.splitlines():
            if "release" in line:
                return line.split("release")[-1].strip().split(",")[0].replace(".", "")
    except Exception:
        return None

def get_index_url(cuda_version):
    if cuda_version == "128":
        return "https://download.pytorch.org/whl/nightly/cu128"
    elif cuda_version == "121":
        return "https://download.pytorch.org/whl/cu121"
    elif cuda_version == "118":
        return "https://download.pytorch.org/whl/cu118"
    else:
        return "https://download.pytorch.org/whl/cpu"  # CPU fallback if no CUDA

def install_torch(index_url):
    print(f"Installing PyTorch from: {index_url}")
    subprocess.run([
        "uv", "pip", "install", "--pre",
        "torch", "torchvision", "torchaudio",
        "--index-url", index_url
    ], check=True)

if __name__ == "__main__":
    if "--dry" in sys.argv or os.getenv("UV_APP_DRY") == "1":
        print("Dry run mode: Skipping PyTorch installation.")
        sys.exit(0)

    cuda = detect_cuda_version()
    print("Detected CUDA:", cuda if cuda else "not found (CPU fallback)")
    install_torch(get_index_url(cuda))
