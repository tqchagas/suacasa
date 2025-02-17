#!/bin/sh

echo "Make migrations..."
python manage.py makemigrations --noinput

echo "Starting container in $DJANGO_ENV..."

# Migrate
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start server (check if it's in development or production)
if [ "$DJANGO_ENV" = "development" ]; then
    echo "Development mode..."
    exec python manage.py runserver 0.0.0.0:8000
else
    echo "Gunicorn mode..."
    exec gunicorn --workers=4 --bind=0.0.0.0:8000 suacasa.wsgi:application
fi
