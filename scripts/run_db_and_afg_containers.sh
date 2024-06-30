#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/
APP_ENV_FILE="${PROJECT_DIR}env/.env"

if [ -f "$APP_ENV_FILE" ]; then
    echo "Loading environment variables from ${APP_ENV_FILE}"
    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$APP_ENV_FILE"
else
    echo "$APP_ENV_FILE env file does not exist"
fi

CALCULATED_PATHS_ENV_FILE=$(cd "${PROJECT_DIR}env/calculated_paths/" && pwd)/.env
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$APP_ENV_FILE" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

required_vars=(
  ENV
  DOCKERHUB_USERNAME
  TMP_UPLOADED_FILES_DIR

  DB_CONTAINER_NAME
  DB_IMAGE_REPO
  DB_IMAGE_TAG
  DB_DATA_DIR
  DB_PORT
  DB_BODZIFY_API_DB_NAME
  DB_SUPERUSER_NAME
  DB_SUPERUSER_PASSWORD

  AUDIO_FINGERPRINTER_CONTAINER_NAME
  AUDIO_FINGERPRINTER_IMAGE_REPO
  AUDIO_FINGERPRINTER_IMAGE_TAG
  AUDIO_FINGERPRINTER_PORT
  AUDIO_FINGERPRINTER_POOL_DIR_SYMLINK_TARGET
)

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set."
    exit 1
  fi
done

echo "Running the database and audio fingerprinter containers..."

docker pull $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_IMAGE_TAG
docker pull $DOCKERHUB_USERNAME/$AUDIO_FINGERPRINTER_IMAGE_REPO:$AUDIO_FINGERPRINTER_IMAGE_TAG

container_ids=$(docker ps -a -q)
if [ -n "$container_ids" ]; then
    docker rm -f $container_ids
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
-e POSTGRES_PORT=$DB_PORT -d $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_IMAGE_TAG

docker run \
--name=$AUDIO_FINGERPRINTER_CONTAINER_NAME \
--volume=$TMP_UPLOADED_FILES_DIR:$AUDIO_FINGERPRINTER_POOL_DIR_SYMLINK_TARGET \
-p $AUDIO_FINGERPRINTER_PORT:$AUDIO_FINGERPRINTER_PORT \
-e ENV=$ENV \
-e APP_PORT=$AUDIO_FINGERPRINTER_PORT \
-d $DOCKERHUB_USERNAME/$AUDIO_FINGERPRINTER_IMAGE_REPO:$AUDIO_FINGERPRINTER_IMAGE_TAG \
gunicorn -w 4 -b 0.0.0.0:$AUDIO_FINGERPRINTER_PORT run:app