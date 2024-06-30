#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: No app env file provided." >&2
    exit 1
fi
APP_ENV_FILE=$1

if [ -z "$2" ]; then
    echo "Error: No base dir provided." >&2
    exit 1
fi
BASE_DIR=$2

if [ -z "$3" ]; then
    echo "Error: No calculated paths env file path provided." >&2
    exit 1
fi
GENERATED_PATHS_ENV_FILE=$3

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/ 2>&1

if [ -f "$APP_ENV_FILE" ]; then
    echo "Loading environment variables from ${APP_ENV_FILE}"
    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$APP_ENV_FILE"
else
    echo "$APP_ENV_FILE env file does not exist" >&2
fi

if $APP_IS_EXPOSED; then
    echo "APP_IS_EXPOSED is set to true"
    required_vars=("MEDIA_DIR" "TMP_UPLOADED_FILES_DIR")
    if $STATIC_FILES_ARE_NEEDED; then
        required_vars+=("STATIC_FILES_DIR")
    fi
    if $DJANGO_LOGS_ARE_NEEDED; then
        required_vars+=("DJANGO_LOG_DIR")
    fi

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            echo "$var is not set" >&2
            exit 1
        fi
    done
else
    echo "APP_IS_EXPOSED is set to false"
    MEDIA_DIR=${BASE_DIR}$MEDIA_DEFAULT_INTERNAL_DIR
    if $STATIC_FILES_ARE_NEEDED; then
        STATIC_FILES_DIR=${BASE_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR
    fi
    if $DJANGO_LOGS_ARE_NEEDED; then
        DJANGO_LOG_DIR=${BASE_DIR}$DJANGO_LOG_DEFAULT_INTERNAL_DIR
    fi
    TMP_UPLOADED_FILES_DIR=${BASE_DIR}$TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR
fi

LIBRARIES_DIR=${MEDIA_DIR}${LIBRARIES_DIR_NAME}/

if [ -f $GENERATED_PATHS_ENV_FILE ]; then
    rm -f $GENERATED_PATHS_ENV_FILE 2>&1
fi
touch $GENERATED_PATHS_ENV_FILE 2>&1

echo "MEDIA_DIR: $MEDIA_DIR"
echo "LIBRARIES_DIR_NAME: $LIBRARIES_DIR_NAME"
echo "LIBRARIES_DIR: $LIBRARIES_DIR"

echo "MEDIA_DIR=$MEDIA_DIR" >> $GENERATED_PATHS_ENV_FILE
echo "LIBRARIES_DIR_NAME=$LIBRARIES_DIR_NAME" >> $GENERATED_PATHS_ENV_FILE
echo "LIBRARIES_DIR=$LIBRARIES_DIR" >> $GENERATED_PATHS_ENV_FILE

if $STATIC_FILES_ARE_NEEDED; then
    echo "STATIC_FILES_DIR: $STATIC_FILES_DIR"
    echo "STATIC_FILES_DIR=$STATIC_FILES_DIR" >> $GENERATED_PATHS_ENV_FILE
else
    echo "STATIC_FILES_ARE_NEEDED is set to false so STATIC_FILES_DIR is not set"
fi

if $DJANGO_LOGS_ARE_NEEDED; then
    echo "DJANGO_LOG_DIR: $DJANGO_LOG_DIR"
    echo "DJANGO_LOG_DIR=$DJANGO_LOG_DIR" >> $GENERATED_PATHS_ENV_FILE
else
    echo "DJANGO_LOGS_ARE_NEEDED is set to false so DJANGO_LOG_DIR is not set"
fi

echo "TMP_UPLOADED_FILES_DIR: $TMP_UPLOADED_FILES_DIR"
echo "TMP_UPLOADED_FILES_DIR=$TMP_UPLOADED_FILES_DIR" >> $GENERATED_PATHS_ENV_FILE
