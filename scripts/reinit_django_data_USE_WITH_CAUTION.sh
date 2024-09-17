#!/bin/bash

# WARNING: This script will reinitialize the Django database.
# Use with caution as it may result in data loss.

load_env_vars () {
  log "Loading environment variables..."
  load_app_env_file_if_exists
  load_project_calculated_paths_env_vars

  local REQUIRED_NON_BOOL_VARS=(
      APP_NAME
      LIBRARIES_DIR
      DB_BODZIFY_API_DB_NAME
      DB_PORT
      DB_SUPERUSER_NAME
      DB_SUPERUSER_PASSWORD
      DB_BODZIFY_API_USERNAME
  )
  check_vars_are_set "${REQUIRED_NON_BOOL_VARS[@]}"
  log "Environment variables loaded successfully."
}

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source ${SCRIPTS_DIR}utils.sh

log "WARNING: This script will reinitialize the Django database."
log "Use with caution as it may result in data loss."
read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

if [ "$CONFIRMATION" != "yes" ]; then
    log "Operation aborted." >&2
    exit 1
fi

load_env_vars

bash ${SCRIPTS_DIR}purge_django_data_USE_WITH_CAUTION.sh -s
if [ $? -ne 0 ]; then
  log "ERROR: Failed to purge data." >&2
  exit 1
fi

bash ${SCRIPTS_DIR}init_django_data.sh
if [ $? -ne 0 ]; then
  log "ERROR: Failed to initialize Django data." >&2
  exit 1
fi

log "Django data reinitialized successfully."