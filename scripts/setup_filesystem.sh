#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_PATH=$(dirname "$SCRIPTS_DIR")/

CALCULATED_PATHS_ENV_FILE="$SCRIPTS_DIR../env/calculated_paths/.env"
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
    echo "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

if [ ! -d "$LIBRARIES_DIR" ]; then
    echo "Creating libraries directory..."
    mkdir -p $LIBRARIES_DIR
else
    echo "Libraries directory $LIBRARIES_DIR already exists"
fi

if [ ! -d "$STATIC_FILES_DIR" ]; then
    echo "Creating static files directory $STATIC_FILES_DIR"
    mkdir -p $STATIC_FILES_DIR
else
    echo "Static files directory $STATIC_FILES_DIR already exists"
fi

if [ ! -d "$LOG_DIR" ]; then
    echo "Creating Django log directory $LOG_DIR"
    mkdir -p $LOG_DIR
else
    echo "Django log directory $LOG_DIR already exists"
fi

touch ${LOG_DIR}requests.log
touch ${LOG_DIR}requests.debug.log
touch ${LOG_DIR}exceptions.log
touch ${LOG_DIR}general.log
touch ${LOG_DIR}info.log
touch ${LOG_DIR}django.log
touch ${LOG_DIR}bodzify-api.log

if [ ! -d "$TMP_UPLOADED_FILES_DIR" ]; then
    echo "Creating temp uploaded files directory $TMP_UPLOADED_FILES_DIR"
    mkdir -p $TMP_UPLOADED_FILES_DIR
else
    echo "Temp uploaded files directory $TMP_UPLOADED_FILES_DIR already exists"
fi

chmod 775 $MEDIA_DIR $STATIC_FILES_DIR $LOG_DIR $TMP_UPLOADED_FILES_DIR