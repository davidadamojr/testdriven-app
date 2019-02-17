#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z users-db 5432; do
   echo "Waiting for Postgres..."
   sleep 0.2
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0