#!/bin/bash

if [ -z "$1" ]; then
    echo "No env file specified"
else
  ENV_FILE="$1"
  if [ ! -f "$ENV_FILE" ]; then
      echo "$ENV_FILE env file does not exist" >&2
      exit 1
  fi

  echo "Loading environment variables from ${ENV_FILE}" >&2
  while IFS='=' read -r key value
  do
      # Skip comments and empty lines
      if [ -z "$key" ]; then continue; fi
      export "$key=$value"
  done < "$ENV_FILE"
fi

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/

cat << EOF > ${SCRIPTS_DIR}$DOCKER_COMPOSE_PART_FILENAME
  db:
    image: $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_IMAGE_TAG
    container_name: $DB_CONTAINER_NAME
    volumes:
      - db-data:$DB_DATA_DIR
      - ./db_init_roles.sql:/db/init_roles.sql
    ports:
      - "$DB_PORT:$DB_PORT"
    networks:
      - bodzify-network
    env_file: $DB_ENV_VARIABLES_FILENAME

  audio_fingerprinter:
    working_dir: /app/
    image: $DOCKERHUB_USERNAME/$AUDIO_FINGERPRINTER_IMAGE_REPO:$AUDIO_FINGERPRINTER_IMAGE_TAG
    container_name: $AUDIO_FINGERPRINTER_CONTAINER_NAME
    volumes:
      - api-upload-temp-files:$AUDIO_FINGERPRINTER_POOL_DIR_SYMLINK_TARGET
      - afg-log-dir:$AUDIO_FINGERPRINTER_LOG_DIR_SYMLINK_TARGET
    ports:
      - "$AUDIO_FINGERPRINTER_PORT:$AUDIO_FINGERPRINTER_PORT"
    networks:
      - bodzify-network
    env_file: $AUDIO_FINGERPRINTER_ENV_FILENAME

  api:
    working_dir: /home/app/webapp/
    image: $DOCKERHUB_USERNAME/$APP_IMAGE_REPO:$APP_IMAGE_TAG
    container_name: $APP_CONTAINER_NAME
    command: >
      gunicorn bodzify_api.wsgi:application
      --bind 0.0.0.0:$APP_PORT
      --error-logfile=${GUNICORN_LOG_DIR}$GUNICORN_LOG_ERROR_FILENAME
      --access-logfile=${GUNICORN_LOG_DIR}$GUNICORN_LOG_ACCESS_FILENAME
      --log-level=info
    volumes:
      - api-django-log-dir:${DJANGO_LOG_DIR}
      - api-gunicorn-log-dir:${GUNICORN_LOG_DIR}
      - api-media-dir:${MEDIA_DIR}
      - api-static-files:${STATIC_FILES_DIR}
      - api-upload-temp-files:${TMP_UPLOADED_FILES_DIR}
    expose:
      - $APP_PORT
    networks:
      - bodzify-network
    depends_on:
      - audio_fingerprinter
      - db
    env_file: $APP_ENV_FILENAME
EOF