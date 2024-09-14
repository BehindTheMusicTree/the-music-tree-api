#!/bin/bash

echo "Initializing database and role"

export_value_removing_surrounding_quotes() {
    local VAR_NAME=$1
    local VAR_VALUE=${!VAR_NAME}
    VAR_VALUE=${VAR_VALUE#\'}
    VAR_VALUE=${VAR_VALUE%\'}
    export "$VAR_NAME=$VAR_VALUE"
}

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
  DB_SUPERUSER_PASSWORD
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

VARS_WITH_EVENTUAL_SURROUNDING_QUOTES=(
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_USER_PASSWORD
)
for VAR in "${VARS_WITH_EVENTUAL_SURROUNDING_QUOTES[@]}"; do
  export_value_removing_surrounding_quotes "$VAR"
done

export PGPASSWORD=$DB_SUPERUSER_PASSWORD

echo "Checking if database $DB_BODZIFY_API_DB_NAME exists"
DB_EXISTS=$(psql -h $DB_HOST -U $DB_SUPERUSER_NAME -tAc \
  "SELECT 1 FROM pg_database WHERE datname='$DB_BODZIFY_API_DB_NAME';" 2>&1)

if [ $? -ne 0 ]; then
  echo "Failed to check if the database exists. Details: $DB_EXISTS" >&2
  exit 1
fi

if [ "$DB_EXISTS" != "1" ]; then
    echo "Database $DB_BODZIFY_API_DB_NAME does not exist. Creating..."
    psql -h $DB_HOST -U $DB_SUPERUSER_NAME -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME;"
else
    echo "Database $DB_BODZIFY_API_DB_NAME already exists."
fi

echo "Creating role $DB_BODZIFY_API_USERNAME"
psql -h $DB_HOST -U $DB_SUPERUSER_NAME -d $DB_BODZIFY_API_DB_NAME -c \
  "CREATE USER $DB_BODZIFY_API_USERNAME WITH PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';"

echo "Granting privileges to role $DB_BODZIFY_API_USERNAME"
psql -h $DB_HOST -U $DB_SUPERUSER_NAME -d $DB_BODZIFY_API_DB_NAME -c \
  "GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME; \
  ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8'; \
  ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed'; \
  ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC'; \
  ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB; \
  GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_BODZIFY_API_USERNAME; \
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_BODZIFY_API_USERNAME;"

echo "Displaying databases to verify that the new database was created"
psql -h $DB_HOST -U $DB_SUPERUSER_NAME -c "\l"

echo "Displaying roles to verify that the new role was created"
psql -h $DB_HOST -U $DB_SUPERUSER_NAME -c "\du"

unset PGPASSWORD