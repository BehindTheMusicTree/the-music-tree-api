#!/bin/bash

echo "Initializing Django data"

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "$SCRIPTS_DIR../")/

# Environment file
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
      done < "$APP_ENV_FILE"
  else
      echo "The provided env file does not exist"
  fi
fi

# Calculated paths environment file
CALCULATED_PATHS_ENV_FILE=${PROJECT_DIR}env/calculated_paths/.env
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

# Required environment variables
REQUIRED_VARS=(
  APP_NAME
  DB_CONTAINER_NAME
  DB_BODZIFY_API_DB_NAME
  DB_SUPERUSER_NAME
  LIBRARIES_DIR
  INIT_DB_AND_ROLE_SCRIPT_NAME
)
for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR}" ]; then
    echo "$VAR must be set." >&2
    exit 1
  fi
done

# Check active connections
ACTIVE_CONNECTIONS=$(docker exec -i $DB_CONTAINER_NAME \
psql -U $DB_SUPERUSER_NAME \
-tAc "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='${DB_BODZIFY_API_DB_NAME}' AND pid <> pg_backend_pid();")

if [ "$ACTIVE_CONNECTIONS" -gt 0 ]; then
    echo "ERROR: Database ${DB_BODZIFY_API_DB_NAME} is being accessed by other users. Aborting." >&2
    exit 1
else
    echo "Database is not being accessed by other users. Proceeding."
fi

# Empty library directory
echo "Empty library directory"
USERS_SUBFOLDERS_COUNT=$(find "$LIBRARIES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
TOTAL_TRACK_FILES_COUNT=$(find "$LIBRARIES_DIR" -mindepth 2 -type f | wc -l)
rm -rf "$LIBRARIES_DIR"*
echo "$USERS_SUBFOLDERS_COUNT user subfolders were deleted."
echo "$TOTAL_TRACK_FILES_COUNT track files were deleted."

# Check if database exists
echo "Check if database exists"
DB_EXISTS=$(docker exec -i $DB_CONTAINER_NAME \
psql -U $DB_SUPERUSER_NAME -tAc "SELECT 1 FROM pg_database WHERE datname='${DB_BODZIFY_API_DB_NAME}'")
if [ "$DB_EXISTS" = "1" ]; then
    echo "Database exists. Dropping database"
    docker exec -i $DB_CONTAINER_NAME \
    psql -U $DB_SUPERUSER_NAME -c "DROP DATABASE $DB_BODZIFY_API_DB_NAME;"
else
    echo "Database does not exist."
fi

# Check if user exists
echo "Check if user exists"
USER_EXISTS=$(docker exec -i $DB_CONTAINER_NAME \
psql -U $DB_SUPERUSER_NAME -tAc "SELECT 1 FROM pg_roles WHERE rolname='${DB_BODZIFY_API_USERNAME}'")
if [ "$USER_EXISTS" = "1" ]; then
    echo "User exists. Dropping user"
    docker exec -i $DB_CONTAINER_NAME \
    psql -U $DB_SUPERUSER_NAME -c "DROP USER $DB_BODZIFY_API_USERNAME;"
else 
    echo "User does not exist."
fi

# Delete migrations
echo "Deleting migrations."
MIGRATIONS_DIR="${PROJECT_DIR}${APP_NAME}/migrations/"
find "${MIGRATIONS_DIR}*.py" -not -name "__init__.py" -delete
find "${MIGRATIONS_DIR}*.pyc"  -delete

# Create database
echo "Creating database."
bash ${SCRIPTS_DIR}${INIT_DB_AND_ROLE_SCRIPT_NAME}

MANAGE_PATH=${PROJECT_DIR}manage.py

# Create initial migrations
echo "Creating initial migrations."
python3 $MANAGE_PATH makemigrations

# Apply migrations
python3 $MANAGE_PATH migrate

# Load all fixture data
python3 $MANAGE_PATH loaddata app admin_user_dev mobile_test_user postman_test_user ultimate_music_guide_test_user_dev