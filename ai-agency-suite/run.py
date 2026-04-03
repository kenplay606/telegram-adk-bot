"""
AI Agency Suite - Main Runner
Starts both backend API and Streamlit dashboard
"""
import subprocess
import sys
import time
import signal
import os

processes = []


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\nShutting down AI Agency Suite...")
    for proc in processes:
        proc.terminate()
    sys.exit(0)


def main():
    """Start backend and dashboard"""
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=" * 60)
    print("  AI AGENCY SUITE - STARTING")
    print("=" * 60)
    
    # Start backend API
    print("\n🚀 Starting backend API...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--reload"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(backend_proc)
    
    # Wait a bit for backend to start
    time.sleep(3)
    
    # Start Streamlit dashboard
    print("🎨 Starting Streamlit dashboard...")
    dashboard_proc = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "dashboard/streamlit_app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    processes.append(dashboard_proc)
    
    print("\n" + "=" * 60)
    print("  AI AGENCY SUITE - RUNNING")
    print("=" * 60)
    print("\n📊 Dashboard: http://localhost:8501")
    print("🔌 API Docs:  http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(None, None)


if __name__ == "__main__":
    main()
