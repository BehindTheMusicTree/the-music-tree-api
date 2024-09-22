#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source ${SCRIPTS_DIR}utils.sh

log "Generating partial docker-compose files..."

# One docker-compose part file for each service so that the Web Server Management add the network name for 
# each one of them separatly.

load_app_env_file_if_exists

REQUIRED_NON_BOOL_VARS=(
  DOCKER_COMPOSE_PART_FILENAME_SUFFIXE
  DOCKERHUB_USERNAME
  DB_IMAGE_REPO
  DB_VERSION
  DB_CONTAINER_NAME
  DB_DATA_DIR
  DB_PORT_HOST
  DB_PORT
  DB_ENV_FILENAME
  AFP_IMAGE_REPO
  AFP_VERSION
  AFP_CONTAINER_NAME
  AFP_PORT
  AFP_ENV_FILENAME
  AFP_POOL_DIR_EXTERNAL
  AFP_FLASK_LOG_DIR_EXTERNAL
  AFP_GUNICORN_LOG_DIR_EXTERNAL
  APP_SERVICE_NAME
  APP_ROOT_DIR
  APP_IMAGE_REPO
  APP_VERSION
  APP_CONTAINER_NAME
  APP_PORT
  APP_ENV_FILENAME
  GUNICORN_LOG_DIR
  DJANGO_LOG_DIR_EXTERNAL
  MEDIA_DIR_EXTERNAL
  STATIC_FILES_EXTERNAL
  TMP_UPLOADED_FILES_EXTERNAL
)
check_vars_are_set ${REQUIRED_NON_BOOL_VARS[@]}

DOCKER_COMPOSE_PART_DB_FILE="${SCRIPTS_DIR}db${DOCKER_COMPOSE_PART_FILENAME_SUFFIXE}"
log "Generating the DB partial docker-compose files in $DOCKER_COMPOSE_PART_DB_FILE..."
cat << EOF > "$DOCKER_COMPOSE_PART_DB_FILE"
  db:
    image: $DOCKERHUB_USERNAME/$DB_IMAGE_REPO:$DB_VERSION
    container_name: $DB_CONTAINER_NAME
    volumes:
      - db-data:$DB_DATA_DIR
    ports:
      - "$DB_PORT_HOST:$DB_PORT"
    env_file: $DB_ENV_FILENAME
EOF
log "DB partial docker-compose file generated."

DOCKER_COMPOSE_PART_AFP_FILE="${SCRIPTS_DIR}afp${DOCKER_COMPOSE_PART_FILENAME_SUFFIXE}"
log "Generating the AFP partial docker-compose files in $DOCKER_COMPOSE_PART_AFP_FILE..."
cat << EOF > "$DOCKER_COMPOSE_PART_AFP_FILE"
  audio_fingerprinter:
    working_dir: /app/
    image: $DOCKERHUB_USERNAME/$AFP_IMAGE_REPO:$AFP_VERSION
    container_name: $AFP_CONTAINER_NAME
    volumes:
      - api-upload-tmp-files:$AFP_POOL_DIR_EXTERNAL
      - afp-flask-log-dir:$AFP_FLASK_LOG_DIR_EXTERNAL
      - afp-gunicorn-log-dir:$AFP_GUNICORN_LOG_DIR_EXTERNAL
    expose:
      - $AFP_PORT
    env_file: $AFP_ENV_FILENAME
EOF
log "AFP partial docker-compose file generated."

DOCKER_COMPOSE_PART_API_FILE="${SCRIPTS_DIR}api${DOCKER_COMPOSE_PART_FILENAME_SUFFIXE}"
log "Generating the API partial docker-compose files in $DOCKER_COMPOSE_PART_API_FILE..."
cat << EOF > "$DOCKER_COMPOSE_PART_API_FILE"
  ${APP_SERVICE_NAME}:
    working_dir: $APP_ROOT_DIR
    image: $DOCKERHUB_USERNAME/$APP_IMAGE_REPO:$APP_VERSION
    container_name: $APP_CONTAINER_NAME
    volumes:
      - api-django-log-dir:${DJANGO_LOG_DIR_EXTERNAL}
      - api-gunicorn-log-dir:${GUNICORN_LOG_DIR}
      - api-media-dir:${MEDIA_DIR_EXTERNAL}
      - api-static-files:${STATIC_FILES_EXTERNAL}
      - api-upload-tmp-files:${TMP_UPLOADED_FILES_EXTERNAL}
    expose:
      - $APP_PORT
    depends_on:
      - audio_fingerprinter
      - db
    env_file: $APP_ENV_FILENAME
EOF
log "API partial docker-compose file generated."
log "Partial docker-compose files generated."