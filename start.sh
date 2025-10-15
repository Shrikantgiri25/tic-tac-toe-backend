#!/bin/bash

# Exit on error
set -e

echo "📦 Waiting for database to be ready..."
# Optional — uncomment if you use Postgres or MySQL in container
# while ! nc -z db 5432; do
#   sleep 1
# done

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "🧹 Collecting static files..."
python manage.py collectstatic --noinput

echo "🌍 Starting Django server..."
gunicorn game_backend.wsgi:application --bind 0.0.0.0:8000
