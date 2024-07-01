#!/bin/bash

echo "Initializing Django data"

SCRIPTS_DIR=$(realpath $(dirname "$0")/../)
PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR../"))/
APP_ENV_FILE="${PROJECT_DIR}env/.env"

if [ -f "$APP_ENV_FILE" ]; then
    echo "Loading environment variables from ${APP_ENV_FILE}"
    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$APP_ENV_FILE"
else
    echo "$APP_ENV_FILE no app env file"
fi

required_vars=(
  DB_BODZIFY_API_DB_NAME
)
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set."
    exit 1
  fi
done

MANAGE_PATH=${PROJECT_DIR}manage.py

# Apply all available migrations
python3 $MANAGE_PATH migrate

# Create migrations for any model changes that haven't been applied yet
python3 $MANAGE_PATH makemigrations

# Apply the newly created migrations
python3 $MANAGE_PATH migrate

# Load all fixture data
python3 $MANAGE_PATH loaddata app admin_user_dev mobile_test_user postman_test_user ultimate_music_guide_test_user_dev