FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY config/requirements-python.txt ./requirements-python.txt
COPY config/requirements-api.txt ./requirements-api.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-python.txt
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 5000

# Set environment
ENV FLASK_APP=api_server.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')"

# Run the API server
CMD ["python", "api_server.py"]
