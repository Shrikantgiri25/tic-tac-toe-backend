# Use official Python image
FROM python:3.12-slim

# Install Node.js and npm for frontend build
RUN apt-get update && apt-get install -y curl git build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy everything
COPY . .

# Make start.sh executable
RUN chmod +x start.sh

# Install backend dependencies
WORKDIR /app/backend
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Build frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build

# Expose port (Railway sets $PORT)
EXPOSE 8000

# Default start command
CMD ["bash", "/app/start.sh"]
