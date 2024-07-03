#!/bin/bash

echo "Initializing Django data"

APP_ENV_FILE=$1
if [ -z "$APP_ENV_FILE" ]; then
  echo "No env file provided"
else
  echo "Env file provided $APP_ENV_FILE"
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

required_vars=(
  APP_NAME
  DB_CONTAINER_NAME
  DB_BODZIFY_API_DB_NAME
  DB_SUPERUSER_NAME
)
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set."
    exit 1
  fi
done

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

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
SCRIPTS_DIR=$(realpath "$SCRIPT_DIR../")/
PROJECT_DIR=$(realpath "$SCRIPTS_DIR../")/
APP_ENV_FILE="${PROJECT_DIR}env/.env"

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