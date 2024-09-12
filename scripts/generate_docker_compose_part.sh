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

required_vars=(
  DOCKER_COMPOSE_PART_FILENAME
  DOCKER_NETWORK_NAME
  DOCKERHUB_USERNAME

  DB_IMAGE_REPO
  DB_VERSION
  DB_CONTAINER_NAME
  DB_DATA_DIR
  DB_PORT
  DB_ENV_FILENAME

  AFP_IMAGE_REPO
  AFP_VERSION
  AFP_CONTAINER_NAME
  AFP_PORT
  AFP_ENV_FILENAME
  AFP_DOCKERIZED_POOL_DIR
  AFP_DOCKERIZED_FLASK_LOG_DIR
  AFP_DOCKERIZED_GUNICORN_LOG_DIR

  APP_SERVICE_NAME
  APP_IMAGE_REPO
  APP_VERSION
  APP_CONTAINER_NAME
  APP_PORT
  APP_ENV_FILENAME
  GUNICORN_LOG_DIR
  GUNICORN_LOG_ERROR_FILENAME
  GUNICORN_LOG_ACCESS_FILENAME
  DJANGO_LOG_DIR
  MEDIA_DIR
  STATIC_FILES_DIR
  TMP_UPLOADED_FILES_DIR
)
for var in "${required_vars[@]}"; do
  if [ -z "${!var}" ]; then
    echo "$var must be set." >&2
    exit 1
  fi
done

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/

cat << EOF > ${SCRIPTS_DIR}$DOCKER_COMPOSE_PART_FILENAME
  db:
    image: $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
    container_name: $DB_CONTAINER_NAME
    volumes:
      - db-data:$DB_DATA_DIR
    ports:
      - "$DB_PORT:$DB_PORT"
    networks:
      - $DOCKER_NETWORK_NAME
    env_file: $DB_ENV_FILENAME

  audio_fingerprinter:
    working_dir: /app/
    image: $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION
    container_name: $AFP_CONTAINER_NAME
    volumes:
      - api-upload-tmp-files-dir:$AFP_DOCKERIZED_POOL_DIR
      - afp-flask-log-dir:$AFP_DOCKERIZED_FLASK_LOG_DIR
      - afp-gunicorn-log-dir:$AFP_DOCKERIZED_GUNICORN_LOG_DIR
    ports:
      - "$AFP_PORT:$AFP_PORT"
    networks:
      - $DOCKER_NETWORK_NAME
    env_file: $AFP_ENV_FILENAME

  ${APP_SERVICE_NAME}:
    working_dir: /home/app/webapp/
    image: $DOCKERHUB_USERNAME/$APP_IMAGE_REPO:$APP_VERSION
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
      - api-static-files-dir:${STATIC_FILES_DIR}
      - api-upload-tmp-files-dir:${TMP_UPLOADED_FILES_DIR}
    expose:
      - $APP_PORT
    networks:
      - $DOCKER_NETWORK_NAME
    depends_on:
      - audio_fingerprinter
      - db
    env_file: $APP_ENV_FILENAME
EOF