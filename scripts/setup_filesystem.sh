#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
echo "SCRIPT_DIR $SCRIPTS_DIR"
PROJECT_PATH=$(dirname "$SCRIPTS_DIR")/

source "${SCRIPTS_DIR}set_paths_env_vars_from_env_and_config.sh"

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