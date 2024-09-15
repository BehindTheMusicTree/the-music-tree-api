#!/bin/bash

check_var_is_set() {
    local var_name=$1
    if [ -z "${!var_name}" ]; then
        echo "$var_name is not set" >&2
        exit 1
    fi
}

REQUIRED_VARS=(
  APP_NAME
  APP_IS_EXPOSED
  DB_SUPERUSER_NAME
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_DB_NAME
  DB_BODZIFY_API_USERNAME
  DB_BODZIFY_API_USER_PASSWORD
)
for VAR in "${REQUIRED_VARS[@]}"; do
  check_var_is_set "$VAR"
done

SCRIPTS_DIR=$(dirname "$0")/
PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
MANAGE_SCRIPT=${PROJECT_DIR}manage.py
echo "MANAGE_SCRIPT: $MANAGE_SCRIPT"
MIGRATIONS_DIR="${PROJECT_DIR}${APP_NAME}/migrations/"

echo "Checking if migrations already exist..."
if [ -d "${MIGRATIONS_DIR}" ] && [ "$(ls -A ${MIGRATIONS_DIR})" ]; then
    echo "Migrations already exist. Aborting."
    exit 1
fi

echo "Running the script to initialize the database and role."
bash ${SCRIPTS_DIR}init_db_and_role.sh
if [ $? -ne 0 ]; then
  echo "The script init_db_and_role.sh failed."
  exit 1
fi

echo "Creating initial migrations."
OUTPUT=$(python3 $MANAGE_SCRIPT makemigrations 2>&1)
echo "$OUTPUT"
if echo "$OUTPUT" | grep -q "Connection refused"; then
    echo "Failed to create migrations due to database connection issue." >&2
    exit 1
fi

echo "Applying migrations."
python3 $MANAGE_SCRIPT migrate

echo "Loading initial data."
python3 $MANAGE_SCRIPT loaddata app admin_user_dev mobile_test_user postman_test_user ultimate_music_guide_test_user_dev

unset PGPASSWORD