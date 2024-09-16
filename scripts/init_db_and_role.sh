#!/bin/bash

load_env_vars () {
  load_project_env_file_if_exists

  local REQUIRED_NON_BOOL_VARS=(
    DB_PORT
    DB_SUPERUSER_NAME
    DB_SUPERUSER_PASSWORD
    DB_BODZIFY_API_DB_NAME
    DB_BODZIFY_API_USERNAME
    DB_BODZIFY_API_USER_PASSWORD
  )
  check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
  check_bool_vars_are_set "APP_IS_EXPOSED"
  export_value_removing_eventual_surrounding_quotes "DB_SUPERUSER_PASSWORD"
  export_value_removing_eventual_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD"
  export PGPASSWORD=$DB_SUPERUSER_PASSWORD
}

echo "Initializing database and role..."

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source ${SCRIPTS_DIR}utils.sh

load_env_vars
determine_db_host_if_not_set
check_if_db_empty_or_exit

echo "Creating database $DB_BODZIFY_API_DB_NAME ..."
output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME;")
if [ $? -ne 0 ]; then
  echo "Failed to create the database: $output"
  exit 1
fi

echo "Creating role $DB_BODZIFY_API_USERNAME ..."
output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -d $DB_BODZIFY_API_DB_NAME -c \
  "CREATE USER $DB_BODZIFY_API_USERNAME WITH PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';")
if [ $? -ne 0 ]; then
  echo "Failed to create the role: $output"
  exit 1
fi

echo "Granting privileges to role $DB_BODZIFY_API_USERNAME"
output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -d $DB_BODZIFY_API_DB_NAME -c \
  "GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME; \
  ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8'; \
  ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed'; \
  ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC'; \
  ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB; \
  GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_BODZIFY_API_USERNAME; \
  GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_BODZIFY_API_USERNAME;")
if [ $? -ne 0 ]; then
  echo "Failed to grant privileges to the role. Details: $output"
  exit 1
fi

echo "Displaying databases to verify that the new database was created"
psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "\l"

echo "Displaying roles to verify that the new role was created"
psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "\du"

unset PGPASSWORD