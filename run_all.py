"""
run_all.py - Launcher script for Intelligent Review Router
Starts both the FastAPI Backend and Streamlit Dashboard concurrently.
"""

import os
import sys
import time
import signal
import subprocess
import urllib.request

def get_python_executable():
    """Find the virtual environment Python interpreter if available."""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    venv_py_win = os.path.join(root_dir, ".venv", "Scripts", "python.exe")
    venv_py_nix = os.path.join(root_dir, ".venv", "bin", "python")
    
    if os.path.exists(venv_py_win):
        return venv_py_win
    if os.path.exists(venv_py_nix):
        return venv_py_nix
    return sys.executable

def wait_for_url(url, timeout=30):
    """Wait until an HTTP endpoint responds with 200 OK."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False

def main():
    python_exe = get_python_executable()
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 65)
    print(" ⚡ Launching Intelligent Review Router & Support Dashboard")
    print("=" * 65)
    print(f"🐍 Python Interpreter: {python_exe}")
    print(f"📂 Root Directory:     {root_dir}\n")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"

    # 1. Start FastAPI Backend
    print("▶️  Starting FastAPI Backend API on port 8000...")
    backend_cmd = [
        python_exe, "-m", "uvicorn", "main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
    ]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=root_dir,
        env=env
    )

    print("⏳ Waiting for FastAPI Backend to initialize...")
    if wait_for_url("http://127.0.0.1:8000/", timeout=30):
        print("✅ FastAPI Backend is Online at http://127.0.0.1:8000")
        print("📖 Interactive API Docs at http://127.0.0.1:8000/docs\n")
    else:
        print("⚠️  Warning: FastAPI is taking longer to start, continuing...\n")

    # 2. Start Streamlit Frontend
    print("▶️  Starting Streamlit Web Dashboard on port 8501...")
    frontend_cmd = [
        python_exe, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501"
    ]
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=root_dir,
        env=env
    )

    print("\n" + "=" * 65)
    print(" 🚀 Services Running:")
    print("    - Streamlit Dashboard:  http://localhost:8501")
    print("    - FastAPI Backend:     http://127.0.0.1:8000")
    print("    - Swagger Docs:        http://127.0.0.1:8000/docs")
    print("=" * 65)
    print("Press Ctrl+C to stop all services.\n")

    def handle_shutdown(signum, frame):
        print("\n🛑 Stopping all services...")
        try:
            frontend_proc.terminate()
        except Exception:
            pass
        try:
            backend_proc.terminate()
        except Exception:
            pass
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        # Keep launcher running while child processes live
        while True:
            if backend_proc.poll() is not None:
                print("❌ Backend process terminated unexpectedly.")
                break
            if frontend_proc.poll() is not None:
                print("❌ Frontend process terminated unexpectedly.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        handle_shutdown(None, None)

if __name__ == "__main__":
    main()

