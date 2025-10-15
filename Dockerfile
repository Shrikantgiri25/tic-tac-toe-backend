# -------------------------------
# Stage 1: Django Backend Build
# -------------------------------
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend source code
COPY backend/ ./backend
COPY start.sh ./start.sh

# Install Python dependencies
RUN python3 -m pip install --upgrade pip
RUN pip install -r backend/requirements.txt

# Make start.sh executable
RUN chmod +x start.sh

# Expose port
EXPOSE ${PORT}

# Start the backend
CMD ["bash", "./start.sh"]
