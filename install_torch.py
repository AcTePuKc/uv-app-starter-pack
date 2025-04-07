# install_torch_uv.py
# ---------------------
# Smart installer for PyTorch based on CUDA version.
# Use --dry or set UV_APP_DRY=1 to skip actual install (for testing or CI).
# ---------------------

# install_torch.py (REVISED)
import subprocess
import sys
import os

def detect_cuda_version():
    try:
        # Try nvcc first
        try:
            output = subprocess.check_output(["nvcc", "--version"], text=True, stderr=subprocess.DEVNULL)
            for line in output.splitlines():
                if "release" in line:
                    version_part = line.split("release")[-1].strip()
                    major_minor = version_part.split(",")[0] # e.g., "12.1"
                    return major_minor.replace(".", "") # "121"
            return None # nvcc found but no version line? Unlikely.
        except FileNotFoundError:
            # Fallback to nvidia-smi if nvcc not found
            output = subprocess.check_output(["nvidia-smi", "--query-gpu=cuda_version", "--format=csv,noheader"], text=True)
            # Output might be "12.1\n"
            if '.' in output:
                parts = output.strip().split('.')
                return parts[0] + parts[1] # "121"
            return None # Unexpected nvidia-smi output
    except (FileNotFoundError, subprocess.CalledProcessError, Exception) as e:
        # print(f"CUDA detection failed: {e}", file=sys.stderr) # Optional debug
        return None

def get_index_url(cuda_version):
    print(f"Determining PyTorch index for detected CUDA version: {cuda_version}")
    # Prioritize official stable wheels from pytorch.org/get-started/locally/
    if cuda_version and int(cuda_version) >= 121:
        # Map CUDA 12.1 and newer to the official stable cu121 wheel index
        # PyTorch doesn't provide wheels for every minor CUDA version (like 12.8)
        # The cu121 wheels are generally compatible with newer CUDA toolkits/drivers.
        print("Mapping to stable PyTorch cu121 index.")
        return "https://download.pytorch.org/whl/cu121"
    elif cuda_version == "118":
        print("Mapping to stable PyTorch cu118 index.")
        return "https://download.pytorch.org/whl/cu118"
    else:
        # No CUDA detected or older/unsupported version
        if cuda_version:
             print(f"CUDA version {cuda_version} detected, but no specific stable PyTorch wheel URL found. Falling back to CPU.", file=sys.stderr)
        else:
             print("No CUDA detected. Falling back to CPU.")
        return "https://download.pytorch.org/whl/cpu"

def install_torch(index_url):
    print(f"Attempting to install PyTorch using index: {index_url}")
    # Keep it simple - install stable torch matching the index.
    # Remove automatic --pre logic. If user wants pre-release, they need a specific URL/command.
    cmd = [
        "uv", "pip", "install",
        "torch", "torchvision", "torchaudio",
        "--index-url", index_url
    ]

    print(f"Running command: {' '.join(cmd)}")
    try:
        # Capture output for debugging
        result = subprocess.run(cmd, check=True, text=True, capture_output=True, encoding='utf-8')
        print("--- UV Install Output ---")
        print(result.stdout)
        if result.stderr:
             print("--- UV Install Error Output (might be warnings) ---", file=sys.stderr)
             print(result.stderr, file=sys.stderr)
        print("-------------------------")
        print("PyTorch installation command finished.")
    except subprocess.CalledProcessError as e:
        print("--- UV Install Failed ---", file=sys.stderr)
        print(f"Command: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"Return Code: {e.returncode}", file=sys.stderr)
        print("\n--- UV Output ---", file=sys.stderr)
        print(e.stdout, file=sys.stderr)
        print("\n--- UV Error ---", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        print("-------------------------", file=sys.stderr)
        print("PyTorch installation failed. Check the errors above.", file=sys.stderr)
        # Decide if failure should stop the whole script
        # sys.exit(1) # Optional: uncomment to make the launcher fail here
        print("Continuing despite PyTorch install failure (if possible)...", file=sys.stderr)


if __name__ == "__main__":
    is_dry_run = "--dry" in sys.argv or os.getenv("UV_APP_DRY") == "1"

    if is_dry_run:
        print("Dry run mode enabled: Simulating PyTorch installation steps.")
        cuda_version_detected = detect_cuda_version()
        print(f"[Dry Run] Detected CUDA: {cuda_version_detected if cuda_version_detected else 'not found'}")
        target_url = get_index_url(cuda_version_detected)
        print(f"[Dry Run] Would target index URL: {target_url}")
        print("[Dry Run] Skipping actual PyTorch installation.")
        sys.exit(0)

    # --- Actual Installation ---
    cuda = detect_cuda_version()
    index = get_index_url(cuda)
    install_torch(index)
    print("PyTorch setup attempt complete.") # Changed wording slightly