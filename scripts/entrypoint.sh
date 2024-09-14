#!/bin/bash

echo "Starting the api container"

set -e

REQUIRES_VARS=(
    INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT
    APP_PORT
    GUNICORN_LOG_DIR
    GUNICORN_LOG_ERROR_FILENAME
    GUNICORN_LOG_ACCESS_FILENAME
)

if [ -z "INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT" ]; then
    echo "INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT must be set." >&2
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