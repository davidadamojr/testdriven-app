docker-compose exec exercises python manage.py recreate_db
docker-compose exec users python manage.py recreate_db
docker-compose exec exercises python manage.py seed_db
docker-compose exec users python manage.py seed_db
