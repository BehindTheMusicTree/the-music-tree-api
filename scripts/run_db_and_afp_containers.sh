#!/bin/bash

echo "Running the database and audio fingerprinter containers."

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/
APP_ENV_FILE="${PROJECT_DIR}env/.env"
source "${SCRIPTS_DIR}utils.sh"

load_project_env_file
load_project_calculated_paths_env_vars

REQUIRED_NON_BOOL_VARS=(
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
  AFP_DOCKERIZED_POOL_DIR
  AFP_PORT
)
check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}
REQUIRED_BOOL_VARS=(
    "DEBUG"
    "APP_IS_EXPOSED"
    "STATIC_FILES_ARE_NEEDED"
    "DJANGO_LOGS_ARE_NEEDED"
    "AUDIO_META_ANALYSE_IS_NEEDED"
)
check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}
export_value_removing_surrounding_quotes "DB_SUPERUSER_PASSWORD"
export_value_removing_surrounding_quotes "DB_BODZIFY_API_USER_PASSWORD"
echo "Environment variables loaded successfully."

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

echo "Running the database and audio fingerprinter containers..."
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

docker run \
--name=$AFP_CONTAINER_NAME \
--volume=$TMP_UPLOADED_FILES:$AFP_DOCKERIZED_POOL_DIR \
-p $AFP_PORT:$AFP_PORT \
-e ENV=$ENV \
-e DEBUG=$DEBUG \
-e APP_PORT=$AFP_PORT \
-d $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION
echo "Containers running successfully."