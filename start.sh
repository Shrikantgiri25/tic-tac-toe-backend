#!/bin/bash

# Backend
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput &
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT &

# Frontend
cd ../frontend
npm install
npm run build
npx serve -s build -l $PORT
