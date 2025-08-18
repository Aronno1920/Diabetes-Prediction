import subprocess
import sys
import uvicorn
import os

if __name__ == "__main__":

    # Start FastAPI app in a subprocess
    fastapi_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
    )

    # Start Locust in another subprocess (point to stress_test/locustfile.py)
    locust_file = os.path.join("stress_test", "locustfile.py")
    locust_proc = subprocess.Popen(
        [sys.executable, "-m", "locust", "-f", locust_file, "--host", "http://127.0.0.1:8000"]
    )

    try:
        fastapi_proc.wait()
        locust_proc.wait()
    except KeyboardInterrupt:
        fastapi_proc.terminate()
        locust_proc.terminate()