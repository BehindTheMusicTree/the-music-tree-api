#!/bin/bash

# WARNING: This script will purge the Django data. Use with caution.

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source ${SCRIPTS_DIR}utils.sh

log "Purging Django data..."

SKIP_CONFIRMATION=false

while getopts ":s" opt; do
  case $opt in
    s)
      SKIP_CONFIRMATION=true
      ;;
    \?)
      log "ERROR: Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [ "$SKIP_CONFIRMATION" != "true" ]; then
    log "WARNING: This script will purge the Django data. Use with caution."
    read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

    if [ "$CONFIRMATION" != "yes" ]; then
        log "Operation aborted." >&2
        exit 1
    fi
fi

APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
ENV_FILE=${APP_DIR}env/.env
CALCULATED_PATHS_ENV_FILE="${APP_DIR}env/calculated_paths/.env"

load_app_env_file_if_exists
load_project_calculated_paths_env_vars

REQUIRED_NON_BOOL_VARS=(
    APP_NAME
    LIBRARIES_DIR
    DB_PORT
    DB_BODZIFY_API_DB_NAME
    DB_SUPERUSER_NAME
    DB_SUPERUSER_PASSWORD
    DB_BODZIFY_API_USERNAME
)
for VAR in "${REQUIRED_NON_BOOL_VARS[@]}"; do
    check_vars_are_set "$VAR"
done
check_bool_vars_are_set APP_IS_EXPOSED

export_value_removing_eventual_surrounding_quotes DB_SUPERUSER_PASSWORD
export PGPASSWORD=$DB_SUPERUSER_PASSWORD

determine_db_host_if_not_set

log "Empty the library directory $LIBRARIES_DIR ..."
USERS_SUBFOLDERS_COUNT=$(find "$LIBRARIES_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
TOTAL_TRACK_FILES_COUNT=$(find "$LIBRARIES_DIR" -mindepth 2 -type f | wc -l)
rm -rf "$LIBRARIES_DIR"*
if [ $? -ne 0 ]; then
	log "ERROR: Failed to empty the library directory." >&2
	exit 1
fi
log "$USERS_SUBFOLDERS_COUNT user subfolders were deleted."
log "$TOTAL_TRACK_FILES_COUNT track files were deleted."

log "Check if database is being accessed by other users"
output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT COUNT(*) FROM pg_stat_activity WHERE datname='${DB_BODZIFY_API_DB_NAME}'" 2>&1)
if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
    log "ERROR: Failed to check if the database is being accessed by other users: $output" >&2
    exit 1
fi
if [ "$output" -gt 0 ]; then
    log "ERROR: Database ${DB_BODZIFY_API_DB_NAME} is being accessed by other users. Abort" >&2
    exit 1
else
    log "Database is not being accessed by other users. Proceeding."
fi

log "Check if database exists"
output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  "SELECT 1 FROM pg_database WHERE datname='${DB_BODZIFY_API_DB_NAME}'" 2>&1)
if [ "$output" = "1" ]; then
    log "Database exists. Dropping database"
    output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc "DROP DATABASE $DB_BODZIFY_API_DB_NAME;" 2>&1)
    if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
      log "ERROR: Failed to drop the database. Details: $output" >&2
      exit 1
    fi
else
    log "Database does not exist."
fi

log "Check if user exists"
output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc \
  	"SELECT 1 FROM pg_roles WHERE rolname='${DB_BODZIFY_API_USERNAME}'" 2>&1)

if [ $? -ne 0 ] || echo "$output" | grep -i "error" > /dev/null; then
	log "ERROR: Failed to check if the user exists: $output" >&2
	exit 1
fi
if [ "$output" = "1" ]; then
    log "User exists. Dropping user"
    output=$(psql -h $DB_HOST -p $DB_PORT -U $DB_SUPERUSER_NAME -tAc "DROP USER $DB_BODZIFY_API_USERNAME;" 2>&1)
    if [ $? -ne 0 ]; then
		log "ERROR: Failed to drop the user: $output" >&2
		exit 1
    fi
else 
    log "User $DB_SUPERUSER_NAME does not exist."
fi

MIGRATIONS_DIR="${APP_DIR}${APP_NAME}/migrations/"
log "Deleting migrations in directory $MIGRATIONS_DIR ..."
log "Deleting .py migrations..."
find "${MIGRATIONS_DIR}" -name "*.py" -not -name "__init__.py" -exec rm -f {} \;
if [ $? -ne 0 ]; then
    log "ERROR: Failed to delete .py migrations" >&2
    exit 1
fi
log ".py migrations deleted successfully."

log "Deleting .pyc migrations..."
find "${MIGRATIONS_DIR}" -name "*.pyc" -exec rm -f {} \;
if [ $? -ne 0 ]; then
    log "ERROR: Failed to delete .pyc migrations" >&2
    exit 1
fi
log ".pyc migrations deleted successfully."

log "Django data purged successfully."