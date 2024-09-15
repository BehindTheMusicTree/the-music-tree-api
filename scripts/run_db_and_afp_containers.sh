#!/bin/bash

echo "Running the database and audio fingerprinter containers."

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/
APP_ENV_FILE="${PROJECT_DIR}env/.env"
source "${SCRIPTS_DIR}utils.sh"

if [ ! -f "$APP_ENV_FILE" ]; then
    echo "$APP_ENV_FILE env file does not exist" >&2
else
    echo "Loading environment variables from $APP_ENV_FILE"
    if [ ! -f "$APP_ENV_FILE" ]; then
        echo "$APP_ENV_FILE env file does not exist" >&2
        exit 1
    fi

    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$APP_ENV_FILE"
fi

CALCULATED_PATHS_ENV_FILE=$(cd "${PROJECT_DIR}env/calculated_paths/" && pwd)/.env
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

REQUIRED_NON_BOOL_VARS=(
  ENV
  DOCKERHUB_USERNAME
  TMP_UPLOADED_FILES_DIR
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
for var in "${REQUIRED_NON_BOOL_VARS[@]}"; do
  check_var_is_set "$var"
done
check_bool_var_is_set "DEBUG"

VARS_WITH_EVENTUAL_SURROUNDING_QUOTES=(
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_USER_PASSWORD
)
for VAR in "${VARS_WITH_EVENTUAL_SURROUNDING_QUOTES[@]}"; do
  export_value_removing_surrounding_quotes "$VAR"
done

echo "Running the database and audio fingerprinter containers."

docker pull $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
docker pull $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION

CONTAINER_IDS=$(docker ps -a -q)
if [ -n "$CONTAINER_IDS" ]; then
    docker rm -f $CONTAINER_IDS
else
    echo "No container to remove."
fi

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
--volume=$TMP_UPLOADED_FILES_DIR:$AFP_DOCKERIZED_POOL_DIR \
-p $AFP_PORT:$AFP_PORT \
-e ENV=$ENV \
-e DEBUG=$DEBUG \
-e APP_PORT=$AFP_PORT \
-d $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION