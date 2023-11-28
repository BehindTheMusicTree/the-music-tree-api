#!/bin/bash

projectDir=~/Git/bodzify-api
managePath=~/Git/bodzify-api/manage.py
dropdb -e bodzify_api -f
createdb bodzify_api
createdb -O django bodzify_api
sudo rm -r $projectDir/bodzify_api/migrations/*
sudo rm -r /var/lib/bodzify-api/*
python3 $managePath migrate
python3 $managePath migrate --fake
python3 $managePath makemigrations 
python3 $managePath migrate
python3 $managePath makemigrations bodzify_api
python3 $managePath migrate
python3 $managePath loaddata app_initial_data
python3 $managePath loaddata admin_user_initial_data
python3 $managePath loaddata mobile_test_user_initial_data
python3 $managePath loaddata postman_test_user_initial_data
python3 $managePath runserver