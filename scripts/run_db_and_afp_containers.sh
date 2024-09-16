#!/bin/bash

load_env_vars () {
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
    check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
    local REQUIRED_BOOL_VARS=(
        "DEBUG"
        "APP_IS_EXPOSED"
        "DB_DATA_MUST_PERSIST"
    )
    check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}
    export_value_removing_eventual_surrounding_quotes "DB_SUPERUSER_PASSWORD"
    export_value_removing_eventual_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD"
    echo "Environment variables loaded successfully."
}

echo "Running the database and audio fingerprinter containers."

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
APP_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/
APP_ENV_FILE="${APP_DIR}env/.env"
source "${SCRIPTS_DIR}utils.sh"

load_env_vars

echo "Pulling the database and audio fingerprinter images..."
docker pull $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
docker pull $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION
echo "Images pulled successfully."

CONTAINER_IDS=$(docker ps -a -q)
if [ -n "$CONTAINER_IDS" ]; then
    echo "Removing existing containers..."
    docker rm -f $CONTAINER_IDS
    echo "Containers removed successfully."
else
    echo "No container to remove."
fi

echo "Running the database container..."
if [ "$DB_DATA_MUST_PERSIST" = true ]; then
    docker run \
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
    docker run \
        --name=$DB_CONTAINER_NAME \
        -p $DB_PORT:$DB_PORT \
        -e ENV=$ENV \
        -e POSTGRES_DB=$DB_BODZIFY_API_DB_NAME \
        -e POSTGRES_USER=$DB_SUPERUSER_NAME \
        -e POSTGRES_PASSWORD=$DB_SUPERUSER_PASSWORD \
        -e POSTGRES_PORT=$DB_PORT \
        -d $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
fi
echo "Database container running successfully."

echo "Running the audio fingerprinter container..."
docker run \
    --name=$AFP_CONTAINER_NAME \
    --volume=$TMP_UPLOADED_FILES:$AFP_POOL_DIR_EXTERNAL \
    -p $AFP_PORT:$AFP_PORT \
    -e ENV=$ENV \
    -e DEBUG=$DEBUG \
    -e APP_PORT=$AFP_PORT \
    -d $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION
echo "Audio fingerprinter container running successfully."

echo "Containers running successfully."