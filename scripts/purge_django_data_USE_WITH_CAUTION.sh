#!/bin/bash

# WARNING: This script will purge the Django data.
# Use with caution.

echo "WARNING: This script will purge the Django data."
echo "Use with caution."
read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

if [ "$CONFIRMATION" != "yes" ]; then
    echo "Operation aborted."
    exit 1
fi

REQUIRED_VARS=(
    APP_NAME
    APP_IS_EXPOSED
    LIBRARIES_DIR
    DB_BODZIFY_API_DB_NAME
    DB_HOST
    DB_PORT
    DB_SUPERUSER_NAME
    DB_SUPERUSER_PASSWORD
    DB_BODZIFY_API_USERNAME
)
for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        echo "$VAR must be set." >&2
        exit 1
    fi
done

export_value_removing_surrounding_quotes() {
    local VAR_NAME=$1
    local VAR_VALUE=${!VAR_NAME}
    VAR_VALUE=${VAR_VALUE#\'}
    VAR_VALUE=${VAR_VALUE%\'}
    export "$VAR_NAME=$VAR_VALUE"
}

if [ "$APP_IS_EXPOSED" = "true" ]; then
  echo "The app is exposed. The database host is the database container name"
  check_var_is_set "DB_CONTAINER_NAME"
  DB_HOST=$DB_CONTAINER_NAME
else
  echo "The app is exposed. The database host is the database URL"
  check_var_is_set "DB_URL"
  DB_HOST=$DB_URL
fi
echo "DB_HOST: $DB_HOST"

export_value_removing_surrounding_quotes DB_SUPERUSER_PASSWORD

CURRENT_SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR=$(realpath "${CURRENT_SCRIPT_DIR}/..")

echo "Empty the library directory $LIBRARIES_DIR ..."
USERS_SUBFOLDERS_COUNT=$(find "$LIBRARIES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
TOTAL_TRACK_FILES_COUNT=$(find "$LIBRARIES_DIR" -mindepth 2 -type f | wc -l)
rm -rf "$LIBRARIES_DIR"*
echo "$USERS_SUBFOLDERS_COUNT user subfolders were deleted."
echo "$TOTAL_TRACK_FILES_COUNT track files were deleted."

if [ "$ACTIVE_CONNECTIONS" -gt 0 ]; then
    echo "ERROR: Database ${DB_BODZIFY_API_DB_NAME} is being accessed by other users. Aborting." >&2
    exit 1
else
    echo "Database is not being accessed by other users. Proceeding."
fi

echo "Check if database exists"
DB_EXISTS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT 1 FROM pg_database WHERE datname='${DB_BODZIFY_API_DB_NAME}'")
if [ "$DB_EXISTS" = "1" ]; then
    echo "Database exists. Dropping database"
    OUTPUT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "DROP DATABASE $DB_BODZIFY_API_DB_NAME;" 2>&1)
    if [ $? -ne 0 ]; then
      echo "Failed to drop the database. Details: $OUTPUT"
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
    OUTPUT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "DROP USER $DB_BODZIFY_API_USERNAME;" 2>&1)
    if [ $? -ne 0 ]; then
      echo "Failed to drop the user. Details: $OUTPUT"
      exit 1
    fi
else 
    echo "User $DB_SUPERUSER_NAME does not exist."
fi

echo "Deleting migrations."
MIGRATIONS_DIR="${PROJECT_DIR}${APP_NAME}/migrations/"
find "${MIGRATIONS_DIR}*.py" -not -name "__init__.py" -delete
find "${MIGRATIONS_DIR}*.pyc"  -delete