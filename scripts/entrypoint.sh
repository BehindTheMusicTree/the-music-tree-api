#!/bin/bash

echo "Starting the api container"

REQUIRES_VARS=(
    INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT
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
    if [ -z "${!VAR}" ]; then
        echo "$VAR must be set." >&2
        exit 1
    fi
done

echo "Running scripts/wait-for-postgres-db.sh to wait for the database..."
OUTPUT=$(bash ${ROOT_DIR}scripts/wait-for-postgres-db.sh $DB_CONTAINER_NAME $DB_PORT $DB_CONNECTION_TEST_MAX_ATTEMPTS $DB_CONNECTION_TEST_SLEEP_INTERVAL)
if [ $? -ne 0 ]; then
    echo "Failed to wait for the database: $OUTPUT" >&2
    exit 1
fi

echo "Database is ready"

echo "Initializing the database and roles if necessary..."
if [ ! -f "${INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT}" ]; then
    echo "${INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT} does not exist" >&2
    exit 1
fi

OUTPUT=$(bash ${INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT})
if [ $? -ne 0 ]; then
    echo "Failed to initialize the database and roles: $OUTPUT" >&2
    exit 1
fi

# Start the application with gunicorn
exec gunicorn bodzify_api.wsgi:application \
    --bind 0.0.0.0:${APP_PORT} \
    --error-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME} \
    --access-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME} \
    --log-level=info