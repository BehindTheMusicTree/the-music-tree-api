SCRPIT_DIR=$(dirname $0)/

cat << EOF > ${SCRPIT_DIR}$DOCKER_COMPOSE_PART_FILENAME
  api:
    working_dir: /home/app/webapp/
    image: $DOCKERHUB_USERNAME/$API_IMAGE_REPO:$API_IMAGE_TAG
    container_name: $API_CONTAINER_NAME
    command: >
      gunicorn bodzify_api.wsgi:application
      --bind 0.0.0.0:8000
      --error-logfile=/home/app/webapp/log/gunicorn/error.log
      --log-level=info
    volumes:
      - api-django-log-dir:/home/app/webapp/log/django/
      - api-gunicorn-log-dir:/home/app/webapp/log/gunicorn/
      - api-media-dir:/home/app/webapp/lib/bodzify-api/media/
      - api-static-files:/home/app/webapp/staticfiles/
      - api-upload-temp-files:/tmp/bodzify-api/uploaded-files/
    expose:
      - 8000
    networks:
      - bodzify-network
    depends_on:
      - audio_fingerprinter
      - db
    env_file: $API_ENV_VARIABLES_FILENAME
EOF