#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# -------------------------
# Backend (Django) setup
# -------------------------
cd backend

# Install Python dependencies
python3 -m pip install --upgrade pip
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# -------------------------
# Frontend (React) build
# -------------------------
cd ../frontend
npm install
npm run build

# -------------------------
# Start backend with Gunicorn
# -------------------------
cd ../backend
gunicorn game_backend.wsgi:application --bind 0.0.0.0:$PORT
