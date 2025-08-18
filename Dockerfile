# 1. Base image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy project files
COPY . .

# 5. Expose port
EXPOSE 8000

# 6. Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]