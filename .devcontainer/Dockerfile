# Use official Python image
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development tools
RUN pip install --no-cache-dir \
    black \
    pylint \
    pytest \
    pytest-cov

# Copy project files
COPY . .

# Set environment variables for development
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN useradd -m vscode && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
USER vscode

# Set up the container for development
CMD ["/bin/bash", "-c", "while true; do sleep 3600; done"]