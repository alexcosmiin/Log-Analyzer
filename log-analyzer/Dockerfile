# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Ensure output directory exists
RUN mkdir -p /app/output

# Default command to run your app
CMD ["python3", "-m", "src.main"]
