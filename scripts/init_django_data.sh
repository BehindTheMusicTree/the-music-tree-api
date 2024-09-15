#!/bin/bash

echo "Initializing Django data..."

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
source ${SCRIPTS_DIR}utils.sh

load_project_env_file

REQUIRED_NON_BOOL_VARS=(
  APP_NAME
  DB_SUPERUSER_NAME
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_DB_NAME
  DB_BODZIFY_API_USERNAME
  DB_BODZIFY_API_USER_PASSWORD
)
check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
check_bool_vars_are_set "APP_IS_EXPOSED"
export_value_removing_surrounding_quotes "DB_SUPERUSER_PASSWORD"
export_value_removing_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD"

MANAGE_SCRIPT=${PROJECT_DIR}manage.py
echo "MANAGE_SCRIPT: $MANAGE_SCRIPT"
MIGRATIONS_DIR="${PROJECT_DIR}${APP_NAME}/migrations/"

echo "Checking if migrations already exist..."
if [ -d "${MIGRATIONS_DIR}" ] && [ "$(find "${MIGRATIONS_DIR}" -type f ! -name '__init__.py' ! -path '*/__pycache__/*' | head -n 1)" ]; then
    echo "Migrations already exist. Aborting..."
    exit 1
fi
echo "Migrations do not exist."

bash ${SCRIPTS_DIR}init_db_and_role.sh

echo "Creating initial migrations..."
OUTPUT=$(python3 $MANAGE_SCRIPT makemigrations 2>&1)
echo "$OUTPUT"
if echo "$OUTPUT" | grep -q "Connection refused"; then
    echo "Failed to create migrations due to database connection issue." >&2
    exit 1
elif echo "$OUTPUT" | grep -q "password authentication failed"; then
    echo "Password authentication failed." >&2
    exit 1
fi
echo "Migrations created successfully."

echo "Applying migrations..."
python3 $MANAGE_SCRIPT migrate
if [ $? -ne 0 ]; then
  echo "Failed to apply migrations. Aborting..." >&2
  exit 1
fi
echo "Migrations applied successfully."

echo "Loading initial data..."
python3 $MANAGE_SCRIPT loaddata app admin_user_dev mobile_test_user postman_test_user ultimate_music_guide_test_user_dev
echo "Initial data loaded successfully."

unset PGPASSWORD