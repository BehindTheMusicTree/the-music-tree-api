#!/bin/bash

echo "Initializing database and role"

if [ -z "$1" ]; then
    echo "No env file specified"
else
    APP_ENV_FILE="$1"
    echo "Loading environment variables from ${APP_ENV_FILE}"
    if [ ! -f "$APP_ENV_FILE" ]; then
        echo "$APP_ENV_FILE env file does not exist" >&2
        exit 1
    fi

    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$APP_ENV_FILE"
fi

echo "DB_CONTAINER_NAME: $DB_CONTAINER_NAME"
required_vars=(
  DB_CONTAINER_NAME
  DB_SUPERUSER_NAME
  DB_BODZIFY_API_DB_NAME
  DB_BODZIFY_API_USERNAME
  DB_BODZIFY_API_USER_PASSWORD
)
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set."
    exit 1
  fi
done

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME;"

# Display all databases
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