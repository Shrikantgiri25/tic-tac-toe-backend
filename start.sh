#!/bin/bash
set -e

# -------------------------
# Backend (Django) setup
# -------------------------
cd /app/backend

python3 -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# -------------------------
# Start backend with Gunicorn
# -------------------------
gunicorn game_backend.wsgi:application --bind 0.0.0.0:$PORT
