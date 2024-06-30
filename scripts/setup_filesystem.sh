#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/
APP_ENV_FILE="${PROJECT_DIR}env/.env"
CALCULATED_PATHS_ENV_FILE=$(realpath "${PROJECT_DIR}env/calculated_paths/.env")
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$APP_ENV_FILE" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading app env from ${APP_ENV_FILE}"
while IFS='=' read -r key value
do
    if [ -z "$key" ]; then continue; fi
    export "$key=$value"
done < "$APP_ENV_FILE"

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
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

if [ -z $STATIC_FILES_DEFAULT_INTERNAL_DIR ]; then
    echo "STATIC_FILES_DEFAULT_INTERNAL_DIR is not set" >&2
    exit 1
fi

DEFAULT_STATIC_FILES_DIR="${PROJECT_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR"
if [ "$STATIC_FILES_DIR" != "$DEFAULT_STATIC_FILES_DIR" ]; then
    echo "STATIC_FILES_DIR is not the default internal directory. Moving static files to $STATIC_FILES_DIR"
    if [ ! -d $DEFAULT_STATIC_FILES_DIR ] or [ find "$DEFAULT_STATIC_FILES_DIR" -mindepth 1 -print -quit | grep -q ]; then
        echo "No static files found in default internal directory $STATIC_FILES_DEFAULT_INTERNAL_DIR"
    else
        mv $DEFAULT_STATIC_FILES_DIR/* $STATIC_FILES_DIR
        echo "Deleting default internal static files directory"
        rm -r $DEFAULT_STATIC_FILES_DIR
    fi
else
    echo "STATIC_FILES_DIR is the default internal directory $DEFAULT_STATIC_FILES_DIR"
fi

if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory $LOG_DIR"
    mkdir -p $LOG_DIR
else
    echo "Log directory $LOG_DIR already exists"
fi

if [ -z $DJANGO_LOG_GENERAL_FILENAME ]; then
    echo "DJANGO_LOG_GENERAL_FILENAME is not set" >&2
    exit 1
fi

if [ -z $DJANGO_LOG_INFO_FILENAME ]; then
    echo "DJANGO_LOG_INFO_FILENAME is not set" >&2
    exit 1
fi

if [ -z $DJANGO_LOG_REQUESTS_FILENAME ]; then
    echo "DJANGO_LOG_REQUESTS_FILENAME is not set" >&2
    exit 1
fi

if [ -z $DJANGO_LOG_REQUESTS_DEBUG_FILENAME ]; then
    echo "DJANGO_LOG_REQUESTS_DEBUG_FILENAME is not set" >&2
    exit 1
fi

if [ -z $DJANGO_LOG_EXCEPTIONS_FILENAME ]; then
    echo "DJANGO_LOG_EXCEPTIONS_FILENAME is not set" >&2
    exit 1
fi

if [ -z $DJANGO_LOG_DJANGO_FILENAME ]; then
    echo "DJANGO_LOG_DJANGO_FILENAME is not set" >&2
    exit 1
fi

if [ -z $DJANGO_LOG_APP_FILENAME ]; then
    echo "DJANGO_LOG_APP_FILENAME is not set" >&2
    exit 1
fi

touch ${LOG_DIR}$DJANGO_LOG_GENERAL_FILENAME
touch ${LOG_DIR}$DJANGO_LOG_INFO_FILENAME
touch ${LOG_DIR}$DJANGO_LOG_REQUESTS_FILENAME
touch ${LOG_DIR}$DJANGO_LOG_REQUESTS_DEBUG_FILENAME
touch ${LOG_DIR}$DJANGO_LOG_EXCEPTIONS_FILENAME
touch ${LOG_DIR}$DJANGO_LOG_DJANGO_FILENAME
touch ${LOG_DIR}$DJANGO_LOG_APP_FILENAME

if [ ! -d "$TMP_UPLOADED_FILES_DIR" ]; then
    echo "Creating temp uploaded files directory $TMP_UPLOADED_FILES_DIR"
    mkdir -p $TMP_UPLOADED_FILES_DIR
else
    echo "Temp uploaded files directory $TMP_UPLOADED_FILES_DIR already exists"
fi

chmod 775 $MEDIA_DIR $STATIC_FILES_DIR $LOG_DIR $TMP_UPLOADED_FILES_DIR