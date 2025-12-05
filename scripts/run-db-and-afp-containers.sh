#!/bin/bash

log_with_script_prefixe () {
    log "[AFP and DB runner] $1"
}

check_script_vars_are_set () {
    load_app_env_file_if_exists
    load_project_calculated_paths_env_vars

    local REQUIRED_NON_BOOL_VARS=(
        ENV
        DOCKERHUB_USERNAME
        LIBRARIES_DIR_NAME
        TMP_UPLOADED_FILES
        DB_CONTAINER_NAME
        DB_IMAGE_REPO
        DB_VERSION
        DB_DATA_DIR
        DB_SUPERUSER_NAME
        DB_SUPERUSER_PASSWORD
        DB_BODZIFY_API_DB_NAME
        DB_BODZIFY_API_USERNAME
        DB_BODZIFY_API_USER_PASSWORD
        DB_PORT
        AFP_CONTAINER_NAME
        AFP_IMAGE_REPO
        AFP_VERSION
        AFP_POOL_DIR_EXTERNAL
        AFP_PORT
    )
    check_required_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
    check_bool_vars_are_set DEBUG APP_IS_EXPOSED DB_DATA_MUST_PERSIST
    export_value_removing_potential_surrounding_quotes DB_SUPERUSER_PASSWORD
    export_value_removing_potential_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD"
    log_with_script_prefixe "Environment variables loaded successfully."
}

main() {
    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/
    APP_ENV_FILE="${PROJECT_DIR}env/.env"
    source "${SCRIPTS_DIR}utils.sh"

    log_with_script_prefixe "Running the database and audio fingerprinter containers..."

    check_script_vars_are_set

    log_with_script_prefixe "Pulling the database and audio fingerprinter images..."
    log_with_script_prefixe $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
    timeout 10 docker pull $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to pull the database image (timeout or error)." >&2
        exit 1
    fi
    timeout 10 docker pull $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to pull the audio fingerprinter image (timeout or error)." >&2
        exit 1
    fi
    log_with_script_prefixe "Images pulled successfully."

    if timeout 10 docker ps -a --format '{{.Names}}' | grep -q "^${DB_CONTAINER_NAME}$"; then
        log_with_script_prefixe "Removing existing database container: $DB_CONTAINER_NAME"
        timeout 30 docker rm -f $DB_CONTAINER_NAME
        if [ $? -ne 0 ]; then
            log_with_script_prefixe "ERROR: Failed to remove database container (timeout or error)." >&2
            exit 1
        fi
        log_with_script_prefixe "Database container removed successfully."
    else
        log_with_script_prefixe "No existing database container to remove."
    fi

    if timeout 10 docker ps -a --format '{{.Names}}' | grep -q "^${AFP_CONTAINER_NAME}$"; then
        log_with_script_prefixe "Removing existing AFP container: $AFP_CONTAINER_NAME"
        timeout 30 docker rm -f $AFP_CONTAINER_NAME
        if [ $? -ne 0 ]; then
            log_with_script_prefixe "ERROR: Failed to remove AFP container (timeout or error)." >&2
            exit 1
        fi
        log_with_script_prefixe "AFP container removed successfully."
    else
        log_with_script_prefixe "No existing AFP container to remove."
    fi

    log_with_script_prefixe "Running the database container..."
    if [ "$DB_DATA_MUST_PERSIST" = true ]; then
        timeout 60 docker run \
            --name=$DB_CONTAINER_NAME \
            --volume=db-data:$DB_DATA_DIR \
            -p $DB_PORT:$DB_PORT \
            -e ENV=$ENV \
            -e POSTGRES_DB=$DB_BODZIFY_API_DB_NAME \
            -e POSTGRES_USER=$DB_SUPERUSER_NAME \
            -e POSTGRES_PASSWORD=$DB_SUPERUSER_PASSWORD \
            -e POSTGRES_PORT=$DB_PORT \
            -d $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
    else
        timeout 60 docker run \
            --name=$DB_CONTAINER_NAME \
            -p $DB_PORT:$DB_PORT \
            -e ENV=$ENV \
            -e POSTGRES_DB=$DB_BODZIFY_API_DB_NAME \
            -e POSTGRES_USER=$DB_SUPERUSER_NAME \
            -e POSTGRES_PASSWORD=$DB_SUPERUSER_PASSWORD \
            -e POSTGRES_PORT=$DB_PORT \
            -d $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
    fi
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to run database container (timeout or error)." >&2
        exit 1
    fi
    log_with_script_prefixe "Database container running successfully."

    log_with_script_prefixe "Running the audio fingerprinter container..."
    timeout 60 docker run \
        --name=$AFP_CONTAINER_NAME \
        --volume=$TMP_UPLOADED_FILES:$AFP_POOL_DIR_EXTERNAL \
        -p $AFP_PORT:$AFP_PORT \
        -e ENV=$ENV \
        -e DEBUG=$DEBUG \
        -e APP_PORT=$AFP_PORT \
        -d $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to run audio fingerprinter container (timeout or error)." >&2
        exit 1
    fi
    log_with_script_prefixe "Audio fingerprinter container running successfully."

    log_with_script_prefixe "Containers running successfully."

    log_with_script_prefixe "Removing unused Docker images..."
    timeout 30 docker image prune -f
    if [ $? -ne 0 ]; then
        log_with_script_prefixe "ERROR: Failed to remove unused Docker images (timeout or error)." >&2
        exit 1
    fi
    log_with_script_prefixe "Unused Docker images removed successfully."
}

main "$@"