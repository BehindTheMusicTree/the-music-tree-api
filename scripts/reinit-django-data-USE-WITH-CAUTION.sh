#!/bin/bash
# WARNING: This script will reinitialize the Django database.
# Use with caution as it may result in data loss.

log_with_script_prefixe () {
    log "[Django data reinitializer] $1"
}

load_env_vars () {
  log_with_script_prefixe "Loading environment variables..."
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
  log_with_script_prefixe "Environment variables loaded successfully."
}

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source ${SCRIPTS_DIR}utils.sh

log_with_script_prefixe "WARNING: This script will reinitialize the Django database."
log_with_script_prefixe "Use with caution as it may result in data loss."

SKIP_CONFIRMATION=false

while getopts ":s" opt; do
case $opt in
	s)
	SKIP_CONFIRMATION=true
	;;
	\?)
	log_with_script_prefixe "ERROR: Invalid option: -$OPTARG" >&2
	exit 1
	;;
esac
done

if [ "$SKIP_CONFIRMATION" != "true" ]; then
	log_with_script_prefixe "WARNING: This script will purge the Django data. Use with caution."
	read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

	if [ "$CONFIRMATION" != "yes" ]; then
		log_with_script_prefixe "Operation aborted." >&2
		exit 1
	fi
fi

load_env_vars

bash ${SCRIPTS_DIR}purge-django-data-USE-WITH-CAUTION.sh -s
if [ $? -ne 0 ]; then
  log_with_script_prefixe "ERROR: Failed to purge data." >&2
  exit 1
fi

bash ${SCRIPTS_DIR}init-django-data.sh
if [ $? -ne 0 ]; then
  log_with_script_prefixe "ERROR: Failed to initialize Django data." >&2
  exit 1
fi

log_with_script_prefixe "Django data reinitialized successfully."