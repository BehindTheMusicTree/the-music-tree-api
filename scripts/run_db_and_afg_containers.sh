#!/bin/bash

echo "Running the database and audio fingerprinter containers."

# Get the directory of the script even when it's called from another script
scripts_dir=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
project_dir=$(realpath $(dirname "$scripts_dir"))/

app_env_file="${project_dir}env/.env"

if [ ! -f "$app_env_file" ]; then
    echo "$app_env_file env file does not exist" >&2
else
    echo "Loading environment variables from $app_env_file"
    if [ ! -f "$app_env_file" ]; then
        echo "$app_env_file env file does not exist" >&2
        exit 1
    fi

    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$app_env_file"
fi

calculated_paths_env_file=$(cd "${project_dir}env/calculated_paths/" && pwd)/.env
bash "${scripts_dir}generate_calculated_paths_env_file.sh" "$project_dir" "$calculated_paths_env_file"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${calculated_paths_env_file}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$calculated_paths_env_file"

required_vars=(
  ENV
  DOCKERHUB_USERNAME

  DEBUG

  TMP_UPLOADED_FILES_DIR

  DB_CONTAINER_NAME
  DB_IMAGE_REPO
  DB_IMAGE_TAG
  DB_DATA_DIR
  DB_SUPERUSER_NAME
  DB_SUPERUSER_PASSWORD
  DB_BODZIFY_API_DB_NAME
  DB_BODZIFY_API_USERNAME
  DB_BODZIFY_API_USER_PASSWORD
  DB_HOST
  DB_PORT

  AUDIO_FINGERPRINTER_CONTAINER_NAME
  AUDIO_FINGERPRINTER_IMAGE_REPO
  AUDIO_FINGERPRINTER_IMAGE_TAG
  AUDIO_FINGERPRINTER_POOL_DIR_SYMLINK_TARGET
  AUDIO_FINGERPRINTER_PORT
)

for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set."
    exit 1
  fi
done

echo "Running the database and audio fingerprinter containers."

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
-e POSTGRES_PORT=$DB_PORT \
-d $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_IMAGE_TAG

docker run \
--name=$AUDIO_FINGERPRINTER_CONTAINER_NAME \
--volume=$TMP_UPLOADED_FILES_DIR:$AUDIO_FINGERPRINTER_POOL_DIR_SYMLINK_TARGET \
-p $AUDIO_FINGERPRINTER_PORT:$AUDIO_FINGERPRINTER_PORT \
-e ENV=$ENV \
-e DEBUG=$DEBUG \
-e APP_PORT=$AUDIO_FINGERPRINTER_PORT \
-d $DOCKERHUB_USERNAME/$AUDIO_FINGERPRINTER_IMAGE_REPO:$AUDIO_FINGERPRINTER_IMAGE_TAG \
gunicorn -w 4 -b 0.0.0.0:$AUDIO_FINGERPRINTER_PORT run:app