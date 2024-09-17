#!/bin/bash

load_env_vars () {
    REQUIRED_NON_BOOL_VARS=(
        APP_PORT
        DB_CONTAINER_NAME
        DB_PORT
        DB_CONNECTION_TEST_MAX_ATTEMPTS
        DB_CONNECTION_TEST_SLEEP_INTERVAL
        DB_SUPERUSER_NAME
        DB_SUPERUSER_PASSWORD
        DB_BODZIFY_API_DB_NAME
        DB_BODZIFY_API_USERNAME
        DB_BODZIFY_API_USER_PASSWORD
        GUNICORN_LOG_DIR
        GUNICORN_LOG_ERROR_FILENAME
        GUNICORN_LOG_ACCESS_FILENAME
    )
    check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
    export_value_removing_eventual_surrounding_quotes "DB_SUPERUSER_PASSWORD"
    export_value_removing_eventual_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD"

    REQUIRED_BOOL_VARS=(
        DEBUG
        APP_IS_EXPOSED
    )
    check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}
}

echo "Starting the api container"

SCRIPTS_DIR=${ROOT_DIR}scripts/
source ${SCRIPTS_DIR}utils.sh

load_env_vars

echo "Running ${SCRIPTS_DIR}wait-for-postgres-db.sh to wait for the database..."
output=$(bash ${SCRIPTS_DIR}wait-for-postgres-db.sh $DB_CONTAINER_NAME $DB_PORT $DB_CONNECTION_TEST_MAX_ATTEMPTS $DB_CONNECTION_TEST_SLEEP_INTERVAL)
if [ $? -ne 0 ]; then
    echo "Failed to wait for the database: $output" >&2
    exit 1
fi
echo "Database is ready"

output=$(bash ${SCRIPTS_DIR}init_django_data.sh)
if [ $? -ne 0 ]; then
    echo "Failed to initialize Django data: $output" >&2
    exit 1
fi

# Start the application with gunicorn
exec gunicorn bodzify_api.wsgi:application \
    --bind 0.0.0.0:${APP_PORT} \
    --error-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME} \
    --access-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME} \
    --log-level=info