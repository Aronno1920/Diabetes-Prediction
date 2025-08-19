# 1. Base image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy project files
COPY . .

# 5. Expose ports (FastAPI + Locust)
EXPOSE 8000 8089

# 6. Run FastAPI + Locust via run_server.py
CMD ["python", "run_server.py"]
