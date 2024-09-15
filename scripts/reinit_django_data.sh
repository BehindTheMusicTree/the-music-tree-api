#!/bin/bash

echo "Initializing Django data"

export_value_removing_surrounding_quotes() {
    local VAR_NAME=$1
    local VAR_VALUE=${!VAR_NAME}
    VAR_VALUE=${VAR_VALUE#\'}
    VAR_VALUE=${VAR_VALUE%\'}
    export "$VAR_NAME=$VAR_VALUE"
}

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "$SCRIPTS_DIR../")/

APP_ENV_FILE=$1
if [ -z "$APP_ENV_FILE" ]; then
  echo "No env file provided as arg. Checking env/.env file"
  APP_ENV_FILE="${PROJECT_DIR}env/.env"
fi
if [ ! -f "$APP_ENV_FILE" ]; then
    echo "env file $APP_ENV_FILE does not exist" >&2
else
  if [ -f "$APP_ENV_FILE" ]; then
      echo "Loading environment variables from ${APP_ENV_FILE}"
      while IFS='=' read -r key value
      do
          # Skip comments and empty lines
          if [ -z "$key" ]; then continue; fi
          export "$key=$value"
          echo "$key=$value"
      done < "$APP_ENV_FILE"
  else
      echo "The provided env file does not exist"
  fi
fi

CALCULATED_PATHS_ENV_FILE=${PROJECT_DIR}env/calculated_paths/.env
echo "Generating calculated paths env file: ${CALCULATED_PATHS_ENV_FILE}"
export DB_IS_NEEDED=true
OUTPUT=$(bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE")
if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file: $OUTPUT" >&2
    exit 1
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

REQUIRED_VARS=(
  APP_NAME
  DB_HOST
  DB_PORT
  DB_BODZIFY_API_DB_NAME
  DB_SUPERUSER_NAME
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_USERNAME
  DB_BODZIFY_API_USER_PASSWORD
  LIBRARIES_DIR
  INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT_NAME
)
for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR}" ]; then
    echo "$VAR must be set." >&2
    exit 1
  fi
done

VARS_WITH_POTENTIAL_SURROUNDING_QUOTES=(
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_USER_PASSWORD
)
for VAR in "${VARS_WITH_POTENTIAL_SURROUNDING_QUOTES[@]}"; do
  export_value_removing_surrounding_quotes "$VAR"
done
export PGPASSWORD=$DB_SUPERUSER_PASSWORD

echo "Empty library directory"
USERS_SUBFOLDERS_COUNT=$(find "$LIBRARIES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
TOTAL_TRACK_FILES_COUNT=$(find "$LIBRARIES_DIR" -mindepth 2 -type f | wc -l)
rm -rf "$LIBRARIES_DIR"*
echo "$USERS_SUBFOLDERS_COUNT user subfolders were deleted."
echo "$TOTAL_TRACK_FILES_COUNT track files were deleted."

echo "Check if database is being accessed by other users"
ACTIVE_CONNECTIONS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='${DB_BODZIFY_API_DB_NAME}' AND pid <> pg_backend_pid();" 2>&1)
if [ $? -ne 0 ]; then
  echo "Failed to check active connections. Details: $ACTIVE_CONNECTIONS"
  exit 1
fi

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
    DROP_DB_OUTPUT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "DROP DATABASE $DB_BODZIFY_API_DB_NAME;" 2>&1)
    if [ $? -ne 0 ]; then
      echo "Failed to drop the database. Details: $DROP_DB_OUTPUT"
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
    DROP_USER_OUTPUT=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "DROP USER $DB_BODZIFY_API_USERNAME;" 2>&1)
    if [ $? -ne 0 ]; then
      echo "Failed to drop the user. Details: $DROP_USER_OUTPUT"
      exit 1
    fi
else 
    echo "User does not exist."
fi

echo "Deleting migrations."
MIGRATIONS_DIR="${PROJECT_DIR}${APP_NAME}/migrations/"
find "${MIGRATIONS_DIR}*.py" -not -name "__init__.py" -delete
find "${MIGRATIONS_DIR}*.pyc"  -delete

echo "Running the script to initialize the database and role."
bash ${SCRIPTS_DIR}${INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT_NAME}
if [ $? -ne 0 ]; then
  echo "The script $INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT_NAME failed."
  exit 1
fi

MANAGE_SCRIPT=${PROJECT_DIR}manage.py
echo "MANAGE_SCRIPT: $MANAGE_SCRIPT"

echo "Creating initial migrations."
MAKEMIGRATIONS_OUTPUT=$(python3 $MANAGE_SCRIPT makemigrations 2>&1)
echo "$MAKEMIGRATIONS_OUTPUT"
if echo "$MAKEMIGRATIONS_OUTPUT" | grep -q "Connection refused"; then
    echo "Failed to create migrations due to database connection issue." >&2
    exit 1
fi

echo "Applying migrations."
python3 $MANAGE_SCRIPT migrate

echo "Loading initial data."
python3 $MANAGE_SCRIPT loaddata app admin_user_dev mobile_test_user postman_test_user ultimate_music_guide_test_user_dev

unset PGPASSWORD