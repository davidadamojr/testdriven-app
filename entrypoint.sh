#!/bin/sh

echo "Waiting for postgres..."

# while ! nc -z users-db 5432; do
#    echo "Waiting for Postgres..."
#    sleep 1
# done

while ! pg_isready -h users-db -p 5432 -q -U postgres; do
   echo "Waiting for postgres - sleeping..." >&2
   sleep 2
done

echo "PostgreSQL started"

python manage.py run -h 0.0.0.0