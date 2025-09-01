# Use Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose Cloud Run port
EXPOSE 8080

# Start with Gunicorn (production-ready)
CMD exec gunicorn --bind :$PORT --workers 2 --threads 8 app:app
