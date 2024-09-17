#!/bin/bash

load_env_vars () {
  load_app_env_file_if_exists

  local REQUIRED_NON_BOOL_VARS=(
    DB_PORT
    DB_SUPERUSER_NAME
    DB_SUPERUSER_PASSWORD
    DB_BODZIFY_API_DB_NAME
    DB_BODZIFY_API_USERNAME
    DB_BODZIFY_API_USER_PASSWORD
  )
  check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
  check_bool_vars_are_set APP_IS_EXPOSED
  export_value_removing_eventual_surrounding_quotes DB_SUPERUSER_PASSWORD
  export_value_removing_eventual_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD"
  export PGPASSWORD=$DB_SUPERUSER_PASSWORD
}

create_database_if_not_exists () {
  echo "Creating database $DB_BODZIFY_API_DB_NAME if it does not exist..."
  echo "Checking if database $DB_BODZIFY_API_DB_NAME exists..."
  output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "SELECT 1 FROM pg_database WHERE datname = '$DB_BODZIFY_API_DB_NAME';" 2>&1)
  if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
    echo "ERROR: Failed to check if the database exists: $output" >&2
    exit 1
  fi
  if [ ! "$output" = "1" ]; then
    echo "Database $DB_BODZIFY_API_DB_NAME does not exist. Creating it..."
    output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME;" 2>&1)
    if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
      echo "FERROR: ailed to create the database: $output" >&2
      exit 1
    fi
  else
    echo "Database $DB_BODZIFY_API_DB_NAME already exists."
  fi
}

create_role_and_grant_permissions_if_not_exists(){
  echo "Creating role $DB_BODZIFY_API_USERNAME if it does not exist..."
  echo "Checking if role $DB_BODZIFY_API_USERNAME exists..."
  local output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -d $DB_BODZIFY_API_DB_NAME -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_BODZIFY_API_USERNAME';" 2>&1)
  if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
    echo "ERROR: Failed to check if the role exists: $output" >&2
    exit 1
  fi
  if [ -n "$output" ]; then
    echo "Role $DB_BODZIFY_API_USERNAME already exists."
  else
    echo "Role $DB_BODZIFY_API_USERNAME does not exist. Creating it..."
    output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -d $DB_BODZIFY_API_DB_NAME -c \
      "CREATE USER $DB_BODZIFY_API_USERNAME WITH PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';" 2>&1)
    if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
      echo "ERROR: Failed to create the role: $output" >&2
      exit 1
    fi
    echo "Role $DB_BODZIFY_API_USERNAME created successfully."
  fi

  echo "Granting privileges to role $DB_BODZIFY_API_USERNAME"
  output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -d $DB_BODZIFY_API_DB_NAME -c \
    "GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME; \
    ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8'; \
    ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed'; \
    ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC'; \
    ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB; \
    GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_BODZIFY_API_USERNAME; \
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_BODZIFY_API_USERNAME;" 2>&1)

  if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
    echo "ERROR: Failed to grant privileges to the role: $output" >&2
    exit 1
  fi
}

main (){
  SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
  source ${SCRIPTS_DIR}utils.sh

  load_env_vars
  determine_db_host_if_not_set
  create_database_if_not_exists
  create_role_and_grant_permissions_if_not_exists

  echo "Displaying databases to verify that the new database was created."
  output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "\l" 2>&1)
  if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
    echo "ERROR: Failed to display databases: $output" >&2
    exit 1
  fi

  echo "Displaying roles to verify that the new role was created."
  output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -c "\du" 2>&1)
  if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
    echo "ERROR: Failed to display roles: $output" >&2
    exit 1
  fi

  unset PGPASSWORD
}

main "$@"
