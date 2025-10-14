# -------------------------------
# Stage 1: Build frontend
# -------------------------------
FROM node:20 AS frontend-builder

# Set working directory
WORKDIR /app/frontend

# Copy only frontend files
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# -------------------------------
# Stage 2: Build backend
# -------------------------------
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend/ ./backend
COPY start.sh ./start.sh

# Install Python dependencies
RUN python3 -m pip install --upgrade pip
RUN pip install -r backend/requirements.txt

# Copy frontend build from previous stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Make start.sh executable
RUN chmod +x start.sh

# Expose port
EXPOSE $PORT

# Start the app
CMD ["bash", "./start.sh"]
