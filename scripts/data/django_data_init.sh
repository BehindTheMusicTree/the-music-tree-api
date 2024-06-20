#!/bin/bash

SCRIPTS_DIR=$(dirname "$0")/../

# Load environment variables in the current shell
source "${SCRIPTS_DIR}load_env_variables.sh"

MANAGE_PATH=$SCRIPTS_DIR../../manage.py
python3 $MANAGE_PATH migrate
python3 $MANAGE_PATH migrate --fake
python3 $MANAGE_PATH makemigrations 
python3 $MANAGE_PATH migrate
python3 $MANAGE_PATH makemigrations bodzify_api
python3 $MANAGE_PATH migrate
python3 $MANAGE_PATH loaddata app
python3 $MANAGE_PATH loaddata admin_user_dev
python3 $MANAGE_PATH loaddata mobile_test_user
python3 $MANAGE_PATH loaddata postman_test_user
python3 $MANAGE_PATH loaddata ultimate_music_guide_test_user_dev