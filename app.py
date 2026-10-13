import os
import sys
import time
import subprocess

def run():
    print("==================================================================")
    print("☸️  Starting KubeMind: Enterprise Agentic RAG on Hugging Face Spaces")
    print("==================================================================")

    # Ensure backend URL is localhost for container internal routing
    os.environ["BACKEND_URL"] = "http://127.0.0.1:8000"

    # 1. Launch FastAPI backend on internal port 8000
    print("📡 Launching FastAPI backend (uvicorn app.main:app on port 8000)...")
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.main:app",
        "--host", "127.0.0.1",
        "--port", "8000",
        "--timeout-graceful-shutdown", "5"
    ])

    # Allow backend time to load NeMo guardrails, LangGraph, and Logfire
    print("⏳ Waiting for backend and guardrails to warm up...")
    time.sleep(5)

    # 2. Launch Streamlit UI on port 7860 (Hugging Face default exposed port)
    print("🎨 Launching Streamlit UI on port 7860...")
    streamlit_cmd = [
        sys.executable, "-m", "streamlit", "run", "ui/app.py",
        "--server.port", "7860",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]

    try:
        subprocess.run(streamlit_cmd, check=True)
    except KeyboardInterrupt:
        print("🛑 Received shutdown signal...")
    finally:
        print("🧹 Terminating background FastAPI backend...")
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()

if __name__ == "__main__":
    run()
