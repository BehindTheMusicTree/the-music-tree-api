#!/bin/bash

# WARNING: This script will purge the Django data. Use with caution.

echo "Purging Django data..."

SKIP_CONFIRMATION=false

while getopts ":s" opt; do
  case $opt in
    s)
      SKIP_CONFIRMATION=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [ "$SKIP_CONFIRMATION" != "true" ]; then
    echo "WARNING: This script will purge the Django data. Use with caution."
    read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

    if [ "$CONFIRMATION" != "yes" ]; then
        echo "Operation aborted."
        exit 1
    fi
fi

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
ENV_FILE=${APP_DIR}env/.env
CALCULATED_PATHS_ENV_FILE="${APP_DIR}env/calculated_paths/.env"
source ${SCRIPTS_DIR}utils.sh

load_app_env_file_if_exists
load_project_calculated_paths_env_vars

REQUIRED_NON_BOOL_VARS=(
    APP_NAME
    LIBRARIES_DIR
    DB_PORT
    DB_BODZIFY_API_DB_NAME
    DB_SUPERUSER_NAME
    DB_SUPERUSER_PASSWORD
    DB_BODZIFY_API_USERNAME
)
for VAR in "${REQUIRED_NON_BOOL_VARS[@]}"; do
    check_vars_are_set "$VAR"
done
check_bool_vars_are_set APP_IS_EXPOSED

export_value_removing_eventual_surrounding_quotes DB_SUPERUSER_PASSWORD
export PGPASSWORD=$DB_SUPERUSER_PASSWORD

determine_db_host_if_not_set

echo "Empty the library directory $LIBRARIES_DIR ..."
USERS_SUBFOLDERS_COUNT=$(find "$LIBRARIES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
TOTAL_TRACK_FILES_COUNT=$(find "$LIBRARIES_DIR" -mindepth 2 -type f | wc -l)
rm -rf "$LIBRARIES_DIR"*
echo "$USERS_SUBFOLDERS_COUNT user subfolders were deleted."
echo "$TOTAL_TRACK_FILES_COUNT track files were deleted."

echo "Check if database is being accessed by other users"
ACTIVE_CONNECTIONS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='${DB_BODZIFY_API_DB_NAME}'")
echo "Active connections: $ACTIVE_CONNECTIONS"
if [ "$ACTIVE_CONNECTIONS" -gt 0 ]; then
    echo "ERROR: Database ${DB_BODZIFY_API_DB_NAME} is being accessed by other users. Abort" >&2
    exit 1
else
    echo "Database is not being accessed by other users. Proceeding."
fi

echo "Check if database exists"
DB_EXISTS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT 1 FROM pg_database WHERE datname='${DB_BODZIFY_API_DB_NAME}'")
if [ "$DB_EXISTS" = "1" ]; then
    echo "Database exists. Dropping database"
    output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "DROP DATABASE $DB_BODZIFY_API_DB_NAME;" 2>&1)
    if [ $? -ne 0 ]; then
      echo "Failed to drop the database. Details: $output"
      exit 1
    fi
else
    echo "Database does not exist."
fi

echo "Check if user exists"
USER_EXISTS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT 1 FROM pg_roles WHERE rolname='${DB_BODZIFY_API_USERNAME}'")
if [ "$USER_EXISTS" = "1" ]; then
    echo "User exists. Dropping user"
    output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "DROP USER $DB_BODZIFY_API_USERNAME;" 2>&1)
    if [ $? -ne 0 ]; then
      echo "Failed to drop the user: $output"
      exit 1
    fi
else 
    echo "User $DB_SUPERUSER_NAME does not exist."
fi

MIGRATIONS_DIR="${APP_DIR}${APP_NAME}/migrations/"
echo "Deleting migrations in directory $MIGRATIONS_DIR ..."
echo "Deleting .py migrations..."
find "${MIGRATIONS_DIR}" -name "*.py" -not -name "__init__.py" -exec rm -f {} \;
if [ $? -ne 0 ]; then
    echo "Failed to delete .py migrations" >&2
    exit 1
fi
echo ".py migrations deleted successfully."

echo "Deleting .pyc migrations..."
find "${MIGRATIONS_DIR}" -name "*.pyc" -exec rm -f {} \;
if [ $? -ne 0 ]; then
    echo "Failed to delete .pyc migrations" >&2
    exit 1
fi
echo ".pyc migrations deleted successfully."

echo "Django data purged successfully."