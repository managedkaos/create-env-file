# Use an official Python runtime as a parent image
FROM python:3.9-slim
LABEL org.opencontainers.image.description="Creates a Docker-style env file from values in AWS Parameter Store."
LABEL org.opencontainers.image.source="https://github.com/managedkaos/create-env-file"
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
RUN pip install -U pip && pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY script.py entrypoint.sh ./

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
