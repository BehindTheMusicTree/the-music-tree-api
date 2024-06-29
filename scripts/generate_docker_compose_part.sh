#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
ENV_PATH="$SCRIPT_DIR../.env"

cat << EOF > ${SCRPIT_DIR}$DOCKER_COMPOSE_PART_FILENAME
  api:
    working_dir: /home/app/webapp/
    image: $DOCKERHUB_USERNAME/$IMAGE_REPO:$IMAGE_TAG
    container_name: $CONTAINER_NAME
    command: >
      gunicorn bodzify_api.wsgi:application
      --bind 0.0.0.0:$APP_PORT
      --error-logfile=${GUNICORN_LOG_DIR}error.log
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
    env_file: $API_ENV_FILENAME
EOF