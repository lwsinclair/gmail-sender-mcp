FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY gmail_sender.py .

# Set environment variables from .env file at runtime
COPY .env.example .env.example

# Run the server
CMD ["python", "gmail_sender.py"]