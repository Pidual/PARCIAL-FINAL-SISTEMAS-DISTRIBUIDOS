FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for persistent data
RUN mkdir -p /app/data

# Copy application code
COPY . .

# Command to run the worker
CMD ["python", "worker.py"]