#!/bin/bash

projectDir=~/git/bodzify-api-django/
managePath=${projectDir}manage.py

# Load env variables from file
export $(grep -v '^#' ${projectDir}.env | xargs)

docker exec -u postgres DB psql -c "CREATE ROLE $DB_BODZIFY_API_USERNAME WITH LOGIN PASSWORD $DB_BODZIFY_API_USER_PASSWORD;"
docker exec -u postgres DB psql -c "DROP DATABASE IF EXISTS $DB_BODZIFY_API_DB_NAME;"
docker exec -u postgres DB psql -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME WITH OWNER $DB_BODZIFY_API_USERNAME;"

sudo rm -r $projectDir/bodzify_api/migrations/*
sudo rm -r $projectDir/media/libraries/*
python3 $managePath migrate
python3 $managePath migrate --fake
python3 $managePath makemigrations 
python3 $managePath migrate
python3 $managePath makemigrations $DB_BODZIFY_API_DB_NAME
python3 $managePath migrate
python3 $managePath loaddata app
python3 $managePath loaddata admin_user_dev
python3 $managePath loaddata mobile_test_user
python3 $managePath loaddata postman_test_user
python3 $managePath loaddata ultimate_music_guide_test_user_dev