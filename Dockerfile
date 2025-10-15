# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (for psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev netcat-traditional && \
    apt-get clean

# Copy dependency files first
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app/

# Make entrypoint script executable
RUN chmod +x /app/start.sh

# Expose the app port
EXPOSE 8000

# Run the startup script
CMD ["/app/start.sh"]
