FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Create logs directory
RUN mkdir -p /app/logs /app/data

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src

# Set environment variables
ENV PYTHONPATH="/app/src:${PYTHONPATH}"

# Create non-root user
RUN useradd -m appuser

# Create set ownership of logs directory to appuser
RUN chown -R appuser:appuser /app/logs /app/data

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8001

# Start the FastAPI server
CMD ["uvicorn", "api.asr_api:app", "--host", "0.0.0.0", "--port", "8001"]