#!/bin/bash

set -e

echo "Initializing database and role"

if [ -z "$1" ]; then
    echo "No ENV file specified as arg."
else
    APP_ENV_FILE="$1"
    echo "Loading environment variables from ${APP_ENV_FILE}"
    if [ ! -f "$APP_ENV_FILE" ]; then
        echo "$APP_ENV_FILE ENV file does not exist"
    else
      while IFS='=' read -r KEY VALUE; do
          # Skip comments and empty lines
          if [[ -z "$KEY" || "$KEY" =~ ^# ]]; then continue; fi
          # Trim whitespace from KEY
          KEY=$(echo "$KEY" | xargs)
          if [ -n "$KEY" ]; then
              export "$KEY=$VALUE"
          fi
      done < "$APP_ENV_FILE"
    fi
fi

echo "DB_CONTAINER_NAME: $DB_CONTAINER_NAME"
REQUIRED_VARS=(
  DB_CONTAINER_NAME
  DB_SUPERUSER_NAME
  DB_BODZIFY_API_DB_NAME
  DB_BODZIFY_API_USERNAME
  DB_BODZIFY_API_USER_PASSWORD
)
for VAR in "${REQUIRED_VARS[@]}"; do
  if [ -z "${!VAR}" ]; then
    echo "$VAR must be set." >&2
    exit 1
  fi
done

DB_EXISTS=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME \
  psql -tAc "SELECT 1 FROM pg_database WHERE datname='$DB_BODZIFY_API_DB_NAME';")

if [ "$DB_EXISTS" != "1" ]; then
    echo "Database $DB_BODZIFY_API_DB_NAME does not exist. Creating..."
    docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME;"
else
    echo "Database $DB_BODZIFY_API_DB_NAME already exists."
fi

DATABASES=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -t -c "SELECT datname FROM pg_database;")

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME \
  psql -d $DB_BODZIFY_API_DB_NAME -c "CREATE USER $DB_BODZIFY_API_USERNAME WITH PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c \
  "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;\"; \
  psql -c \"ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';\"; \
  psql -c \"ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';\"; \
  psql -c \"ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';\"; \
  psql -c \"ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;\"; \
  psql -d $DB_BODZIFY_API_DB_NAME -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_BODZIFY_API_USERNAME;\"; \
  psql -d $DB_BODZIFY_API_DB_NAME -c \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_BODZIFY_API_USERNAME;\""

# List all databases to verify that the new database was created
docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -c "\l"

# List all roles to verify that the new role was created
docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -c "\du"