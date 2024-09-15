#!/bin/bash

# WARNING: This script will reinitialize the Django database.
# Use with caution as it may result in data loss.

echo "WARNING: This script will reinitialize the Django database."
echo "Use with caution as it may result in data loss."
read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

if [ "$CONFIRMATION" != "yes" ]; then
    echo "Operation aborted."
    exit 1
fi

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
  APP_IS_EXPOSED
  DB_PORT
  DB_BODZIFY_API_DB_NAME
  DB_SUPERUSER_NAME
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_USERNAME
  DB_BODZIFY_API_USER_PASSWORD
  LIBRARIES_DIR
)
for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR}" ]; then
    echo "$VAR must be set." >&2
    exit 1
  fi
done

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

VARS_WITH_POTENTIAL_SURROUNDING_QUOTES=(
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_USER_PASSWORD
)
for VAR in "${VARS_WITH_POTENTIAL_SURROUNDING_QUOTES[@]}"; do
  export_value_removing_surrounding_quotes "$VAR"
done
export PGPASSWORD=$DB_SUPERUSER_PASSWORD

echo "Check if database is being accessed by other users"
ACTIVE_CONNECTIONS=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='${DB_BODZIFY_API_DB_NAME}' AND pid <> pg_backend_pid();" 2>&1)
if [ $? -ne 0 ]; then
  echo "Failed to check active connections. Details: $ACTIVE_CONNECTIONS"
  exit 1
fi

OUTPUT=$(bash ${SCRIPTS_DIR}purge_django_data_USE_WITH_CAUTION.sh)
if [ $? -ne 0 ]; then
  echo "Failed to purge Django data. Details: $OUTPUT"
  exit 1
fi

dfgz