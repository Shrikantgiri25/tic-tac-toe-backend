#!/bin/bash
set -e

echo "🚀 Starting Django setup..."

# Move into backend folder
cd /app/backend

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Daphne server (ASGI for WebSockets)
echo "🎯 Starting Daphne server..."
daphne -b 0.0.0.0 -p ${PORT:-8000} game_backend.asgi:application
