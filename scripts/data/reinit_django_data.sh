#!/bin/bash

echo "Initializing Django data"

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
SCRIPTS_DIR=$(realpath "$SCRIPT_DIR../")/
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
      done < "$APP_ENV_FILE"
  else
      echo "The provided env file does not exist"
  fi
fi

CALCULATED_PATHS_ENV_FILE=${PROJECT_DIR}env/calculated_paths/.env
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

required_vars=(
  APP_NAME
  DB_CONTAINER_NAME
  DB_BODZIFY_API_DB_NAME
  DB_SUPERUSER_NAME
  LIBRARIES_DIR
)
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set."
    exit 1
  fi
done

ACTIVE_CONNECTIONS=$(docker exec -i $DB_CONTAINER_NAME \
psql -U $DB_SUPERUSER_NAME \
-tAc "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='${DB_BODZIFY_API_DB_NAME}' AND pid <> pg_backend_pid();")

if [ "$ACTIVE_CONNECTIONS" -gt 0 ]; then
    echo "ERROR: Database ${DB_BODZIFY_API_DB_NAME} is being accessed by other users. Aborting."
    exit 1
else
    echo "Database is not being accessed by other users. Proceeding."
fi

echo "Empty library directory"
users_subfolders_count=$(find "$LIBRARIES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
total_track_files_count=$(find "$LIBRARIES_DIR" -mindepth 2 -type f | wc -l)
rm -rf "$LIBRARIES_DIR"*
echo "$users_subfolders_count user subfolders were deleted."
echo "$total_track_files_count track files were deleted."

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

Echo "Deleting migrations."
MIGRATIONS_DIR="${PROJECT_DIR}${APP_NAME}/migrations/"
find "${MIGRATIONS_DIR}*.py" -not -name "__init__.py" -delete
find "${MIGRATIONS_DIR}*.pyc"  -delete

echo "Creating database."
bash ${SCRIPT_DIR}init_db_and_role.sh

MANAGE_PATH=${PROJECT_DIR}manage.py

echo "Creating initial migrations."
python3 $MANAGE_PATH makemigrations

# Apply migrations
python3 $MANAGE_PATH migrate

# Load all fixture data
python3 $MANAGE_PATH loaddata app admin_user_dev mobile_test_user postman_test_user ultimate_music_guide_test_user_dev