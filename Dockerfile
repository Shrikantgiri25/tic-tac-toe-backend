# Stage 1: Build React frontend
FROM node:20 AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Build Python backend
FROM python:3.12-slim
WORKDIR /app/backend

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./

# Copy built frontend into backend static files (if using Django)
COPY --from=frontend /app/frontend/build ./static

# Set environment variables (Railway will override)
ENV PORT=8000

# Expose port
EXPOSE 8000

# Run Django server with Gunicorn
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
