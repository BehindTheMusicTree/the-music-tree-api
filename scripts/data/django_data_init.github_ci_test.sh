#!/bin/bash

projectDir=./
managePath=$projectDir/manage.py
python3 $managePath migrate
python3 $managePath migrate --fake
python3 $managePath makemigrations 
python3 $managePath migrate
python3 $managePath makemigrations bodzify_api
python3 $managePath migrate
python3 $managePath loaddata app
python3 $managePath loaddata admin_user_dev
python3 $managePath loaddata mobile_test_user
python3 $managePath loaddata postman_test_user
python3 $managePath loaddata ultimate_music_guide_test_user_dev