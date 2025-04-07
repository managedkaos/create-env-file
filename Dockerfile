# Use an official Python runtime as a parent image
FROM python:3.9-slim
ENV PROJECT_HOME=/data
RUN mkdir /data

# Set the working directory in the container
WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY script.py entrypoint.sh .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
