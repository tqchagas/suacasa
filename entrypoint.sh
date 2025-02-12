#!/bin/sh

echo "Make migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "Runserver...."
python manage.py runserver 0.0.0.0:8000