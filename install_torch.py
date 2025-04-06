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
        # Use nvidia-smi for broader compatibility if nvcc isn't installed everywhere
        # Though nvcc is needed for *development*, nvidia-smi is often present with drivers
        # Prioritize nvcc if available
        try:
            output = subprocess.check_output(["nvcc", "--version"], text=True, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
             # Fallback to nvidia-smi if nvcc not found
             output = subprocess.check_output(["nvidia-smi", "--query-gpu=cuda_version", "--format=csv,noheader"], text=True)
             # nvidia-smi might output something like "12.1\n"
             version_str = output.strip().split('.')[0] + output.strip().split('.')[1] if '.' in output else None
             return version_str # e.g. "121"

        # If nvcc worked, parse its output
        for line in output.splitlines():
            if "release" in line:
                # Example: "Cuda compilation tools, release 12.1, V12.1.105"
                version_part = line.split("release")[-1].strip() # "12.1, V12.1.105"
                major_minor = version_part.split(",")[0] # "12.1"
                return major_minor.replace(".", "") # "121"
        return None # Should not happen if nvcc output is standard, but safety first
    except (FileNotFoundError, subprocess.CalledProcessError, Exception) as e:
        # Catch specific errors if preferred, or general Exception
        # print(f"CUDA detection failed: {e}", file=sys.stderr) # Optional debug info
        return None

def get_index_url(cuda_version):
    # Map versions to known PyTorch wheel indices
    # Check PyTorch website for currently supported CUDA versions for wheels
    if cuda_version == "121": # Common stable version
        return "https://download.pytorch.org/whl/cu121"
    elif cuda_version == "118": # Older stable version
        return "https://download.pytorch.org/whl/cu118"
    # Add other versions as needed, e.g., PyTorch might add 12.4 wheels later
    # elif cuda_version == "124":
    #     return "https://download.pytorch.org/whl/cu124" # Example, check if exists
    elif cuda_version and int(cuda_version) >= 125: # Heuristic for future/nightly?
        # Decide if you want to point bleeding edge CUDA to nightly or a specific recent build
        print(f"Detected CUDA {cuda_version}. Attempting nightly build (may be unstable).")
        return "https://download.pytorch.org/whl/nightly/cu121" # Often nightly is built against a specific recent CUDA like 12.1 or newer
        # Or maybe point to the latest known stable wheel instead? Depends on goal.
        # return "https://download.pytorch.org/whl/cu121" # Safer fallback
    else: # No CUDA detected or version not specifically handled
        if cuda_version:
             print(f"CUDA version {cuda_version} detected, but no specific PyTorch wheel URL found. Falling back to CPU.", file=sys.stderr)
        return "https://download.pytorch.org/whl/cpu"  # CPU fallback

def install_torch(index_url):
    print(f"Attempting to install PyTorch using index: {index_url}")
    cmd = [
        "uv", "pip", "install",
        # Pinning specific versions might be safer in production
        "torch", "torchvision", "torchaudio",
        "--index-url", index_url
    ]
    # Conditional --pre logic is good, keep it
    if "nightly" in index_url:
         print("Adding --pre flag for nightly build.")
         # Ensure '--pre' is inserted correctly after 'install'
         cmd.insert(cmd.index("install") + 1, "--pre")

    print(f"Running command: {' '.join(cmd)}") # Show the command being run
    try:
        subprocess.run(cmd, check=True, text=True, capture_output=True) # Capture output for better debugging
        print("PyTorch installation seems successful.")
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
        sys.exit(1) # Exit with error code if install fails


if __name__ == "__main__":
    is_dry_run = "--dry" in sys.argv or os.getenv("UV_APP_DRY") == "1"

    if is_dry_run:
        print("Dry run mode enabled: Simulating PyTorch installation steps.")
        cuda_version_detected = detect_cuda_version()
        print(f"[Dry Run] Detected CUDA: {cuda_version_detected if cuda_version_detected else 'not found'}")
        target_url = get_index_url(cuda_version_detected)
        print(f"[Dry Run] Would target index URL: {target_url}")
        print("[Dry Run] Skipping actual PyTorch installation.")
        sys.exit(0) # Successful exit for dry run

    # --- Actual Installation ---
    cuda = detect_cuda_version()
    print("Detected CUDA:", cuda if cuda else "not found (CPU fallback)")
    index = get_index_url(cuda)
    install_torch(index)
    print("PyTorch setup complete.")