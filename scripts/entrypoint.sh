#!/bin/bash

echo "Starting the api container"

SCRIPTS_DIR=${ROOT_DIR}scripts/
source ${SCRIPTS_DIR}utils.sh

REQUIRES_VARS=(
    APP_PORT
    APP_IS_EXPOSED
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
for VAR in "${REQUIRES_VARS[@]}"; do
    check_var_is_set "$VAR"
done

echo "Running ${SCRIPTS_DIR}wait-for-postgres-db.sh to wait for the database..."
OUTPUT=$(bash ${SCRIPTS_DIR}wait-for-postgres-db.sh $DB_CONTAINER_NAME $DB_PORT $DB_CONNECTION_TEST_MAX_ATTEMPTS $DB_CONNECTION_TEST_SLEEP_INTERVAL)
if [ $? -ne 0 ]; then
    echo "Failed to wait for the database: $OUTPUT" >&2
    exit 1
fi
echo "Database is ready"

OUTPUT=$(bash ${SCRIPTS_DIR}init_django_data.sh)
if [ $? -ne 0 ]; then
    echo "Failed to initialize Django data: $OUTPUT" >&2
    exit 1
fi

# Start the application with gunicorn
exec gunicorn bodzify_api.wsgi:application \
    --bind 0.0.0.0:${APP_PORT} \
    --error-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME} \
    --access-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME} \
    --log-level=info