#!/bin/bash

sudo -u postgres dropdb -e bodzify_api -f
sudo -u postgres -H -- psql -c "create database bodzify_api with owner django;"

docker exec BODZIFY_API python manage.py migrate
docker exec BODZIFY_API python manage.py migrate --fake
docker exec BODZIFY_API python manage.py makemigrations
docker exec BODZIFY_API python manage.py migrate --fake-initial
docker exec BODZIFY_API python manage.py makemigrations bodzify_api
docker exec BODZIFY_API python manage.py migrate
docker exec BODZIFY_API python manage.py loaddata app
docker exec BODZIFY_API python manage.py loaddata admin_user_test
docker exec BODZIFY_API python manage.py loaddata mobile_test_user
docker exec BODZIFY_API python manage.py loaddata postman_test_user
docker exec BODZIFY_API python manage.py loaddata ultimate_music_guide_test_user_test