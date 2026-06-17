FROM python:3.10

WORKDIR /app

# Copy dependencies first (better cache usage)
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Install Chromium + driver + required libs
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY main.py /app

# Default command
CMD ["python", "main.py"]