# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Start with Gunicorn (Cloud Run listens on port 8080)
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app
