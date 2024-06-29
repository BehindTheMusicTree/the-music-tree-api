#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source "$SCRIPT_DIR../../env/.env"

echo "run_db_and_afg_containers.sh: Running the database and audio fingerprinter containers..."
printenv | grep "AUDIO_FINGERPRINTER"

docker pull $DOCKERHUB_USERNAME/$AUDIO_FINGERPRINTER_IMAGE_REPO:$AUDIO_FINGERPRINTER_IMAGE_TAG
docker pull $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_IMAGE_TAG

docker rm $(docker ps -a -q) -f

docker run -p $AUDIO_FINGERPRINTER_PORT:$AUDIO_FINGERPRINTER_PORT \
--volume=$TMP_UPLOADED_FILES_DIR:$AUDIO_FINGERPRINTER_POOL_SYMLINK_TARGET \
-p $AUDIO_FINGERPRINTER_PORT:$AUDIO_FINGERPRINTER_PORT \
-e ENV=$ENV \
-e APP_PORT=$AUDIO_FINGERPRINTER_PORT \
-d $DOCKERHUB_USERNAME/$AUDIO_FINGERPRINTER_IMAGE_REPO:$AUDIO_FINGERPRINTER_IMAGE_TAG \
gunicorn -w 4 -b 0.0.0.0:$AUDIO_FINGERPRINTER_PORT run:app

docker run \
ty--name=$DB_CONTAINER_NAME \
--volume=db-data:$DB_DATA_DIR \
-p $DB_PORT:$DB_PORT \
-e ENV=$ENV \
-e POSTGRES_DB=$DB_BODZIFY_API_DB_NAME \
-e POSTGRES_USER=$DB_SUPERUSER_NAME\
-e POSTGRES_PASSWORD=$DB_SUPERUSER_PASSWORD \
-e POSTGRES_PORT=$DB_PORT \