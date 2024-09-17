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
    check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]} 2>&1
    if [ $? -ne 0 ]; then
        log "ERROR: Failed to load environment variables." >&2
        exit 1
    fi

    export_value_removing_eventual_surrounding_quotes DB_SUPERUSER_PASSWORD 2>&1
    export_value_removing_eventual_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD" 2>&1

    check_bool_vars_are_set DEBUG APP_IS_EXPOSED 2>&1
    if [ $? -ne 0 ]; then
        log "ERROR: Failed to load boolean environment variables." >&2
        exit 1
    fi
}

main (){
    SCRIPTS_DIR=${ROOT_DIR}scripts/
    source ${SCRIPTS_DIR}utils.sh 2>&1
    
    log "Starting the api container"

    load_env_vars 2>&1

    log "Running ${SCRIPTS_DIR}wait-for-postgres-db.sh to wait for the database..."
    output=$(bash ${SCRIPTS_DIR}wait-for-postgres-db.sh $DB_CONTAINER_NAME $DB_PORT $DB_CONNECTION_TEST_MAX_ATTEMPTS $DB_CONNECTION_TEST_SLEEP_INTERVAL 2>&1)
    if [ $? -ne 0 ]; then
        log "Failed to wait for the database: $output" >&2
        exit 1
    fi
    log "Database is ready"

    output=$(bash ${SCRIPTS_DIR}init_django_data.sh 2>&1)
    if [ $? -ne 0 ]; then
        log "Failed to initialize Django data: $output" >&2
        exit 1
    fi

    # Start the application with gunicorn
    exec gunicorn bodzify_api.wsgi:application \
        --bind 0.0.0.0:${APP_PORT} \
        --error-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME} \
        --access-logfile=${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME} \
        --log-level=info 2>&1
}

main "$@" 2>&1