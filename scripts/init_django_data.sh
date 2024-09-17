#!/bin/bash

load_env_vars() {
  log "Loading environment variables..."
  load_app_env_file_if_exists
  local REQUIRED_NON_BOOL_VARS=(
    APP_NAME
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
  log "Environment variables loaded successfully."
}

exit_if_migrations_exist() {
  log "Checking if migrations already exist..."
  local MIGRATIONS_DIR="${APP_DIR}${APP_NAME}/migrations/"
  if [ -d "${MIGRATIONS_DIR}" ] && [ "$(find "${MIGRATIONS_DIR}" -type f ! -name '__init__.py' ! -path '*/__pycache__/*' | head -n 1)" ]; then
      log "ERROR: Migrations already exist. Abort" >&2
      exit 1
  fi
  log "Migrations do not exist."
}

create_initial_migration() {
  log "Creating initial migrations..."
  output=$(python3 $MANAGE_SCRIPT makemigrations 2>&1)
  log "$output"
  if echo "$output" | grep -q "Connection refused"; then
      log "Failed to create migrations due to database connection issue." >&2
      exit 1
  elif echo "$output" | grep -q "password authentication failed"; then
      log "ERROR: Password authentication failed." >&2
      exit 1
  fi
  log "Migrations created successfully."
}

apply_migrations() {
  log "Applying migrations..."
  python3 $MANAGE_SCRIPT migrate
  if [ $? -ne 0 ]; then
    log "ERROR: Failed to apply migrations. Abort" >&2
    exit 1
  fi
  log "Migrations applied successfully."
}

main (){
  SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
  APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
  source ${SCRIPTS_DIR}utils.sh

  log "Initializing Django data..."

  load_env_vars
  exit_if_migrations_exist

  MANAGE_SCRIPT=${APP_DIR}manage.py
  log "MANAGE_SCRIPT: $MANAGE_SCRIPT"

  bash ${SCRIPTS_DIR}init_db_and_role.sh
  if [ $? -ne 0 ]; then
    log "ERROR: Failed to initialize database and role." >&2
    exit 1
  fi

  create_initial_migration
  apply_migrations

  log "Loading initial data..."
  python3 $MANAGE_SCRIPT loaddata app admin_user_dev mobile_test_user postman_test_user ultimate_music_guide_test_user_dev
  log "Initial data loaded successfully."

  unset PGPASSWORD

  log "Django data initialized successfully."
}

main "$@"
