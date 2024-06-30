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

if [ -z $EXTERNAL_DIRS_ARE_NEEDED ]; then
    echo "EXTERNAL_DIRS_ARE_NEEDED is not set." >&2
    exit 1
elif [ "$EXTERNAL_DIRS_ARE_NEEDED" != "true" ] && [ "$EXTERNAL_DIRS_ARE_NEEDED" != "false" ]; then
    echo "EXTERNAL_DIRS_ARE_NEEDED must be 'true' or 'false'." >&2
    exit 1
fi

if [ -z $DJANGO_LOGS_ARE_NEEDED ]; then
    echo "DJANGO_LOGS_ARE_NEEDED is not set." >&2
    exit 1
elif [ "$DJANGO_LOGS_ARE_NEEDED" != "true" ] && [ "$DJANGO_LOGS_ARE_NEEDED" != "false" ]; then
    echo "EXTERNAL_DIRS_ARE_NEEDED must be 'true' or 'false'." >&2
    exit 1
fi

if [ -z $LIBRARIES_DIR_NAME ]; then
    echo "LIBRARIES_DIR_NAME is not set" >&2
    exit 1
fi

if $EXTERNAL_DIRS_ARE_NEEDED; then
    echo "EXTERNAL_DIRS_ARE_NEEDED is set to true"
    if [ -z $MEDIA_DIR ]; then
        echo "MEDIA_DIR is not set" >&2
        exit 1
    fi

    if [ -z $STATIC_FILES_DIR ]; then
        echo "STATIC_FILES_DIR is not set" >&2
        exit 1
    fi

    if [ -z $LOG_DIR ]; then
        echo "LOG_DIR is not set" >&2
        exit 1
    fi

    if [ -z $TMP_UPLOADED_FILES_DIR ]; then
        echo "TMP_UPLOADED_FILES_DIR is not set" >&2
        exit 1
    fi
else
    echo "EXTERNAL_DIRS_ARE_NEEDED is set to false"
    MEDIA_DIR=${BASE_DIR}$MEDIA_DEFAULT_INTERNAL_DIR
    STATIC_FILES_DIR=${BASE_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR
    LOG_DIR=${BASE_DIR}$DJANGO_LOG_DEFAULT_INTERNAL_DIR
    TMP_UPLOADED_FILES_DIR=${BASE_DIR}$TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR
fi

LIBRARIES_DIR=${MEDIA_DIR}${LIBRARIES_DIR_NAME}/

echo "MEDIA_DIR: $MEDIA_DIR"
echo "LIBRARIES_DIR_NAME: $LIBRARIES_DIR_NAME"
echo "LIBRARIES_DIR: $LIBRARIES_DIR"
echo "STATIC_FILES_DIR: $STATIC_FILES_DIR"
echo "LOG_DIR: $LOG_DIR"
echo "TMP_UPLOADED_FILES_DIR: $TMP_UPLOADED_FILES_DIR"

if [ -f $GENERATED_PATHS_ENV_FILE ]; then
    rm -f $GENERATED_PATHS_ENV_FILE 2>&1
fi
touch $GENERATED_PATHS_ENV_FILE 2>&1
echo "MEDIA_DIR=$MEDIA_DIR" >> $GENERATED_PATHS_ENV_FILE
echo "LIBRARIES_DIR_NAME=$LIBRARIES_DIR_NAME" >> $GENERATED_PATHS_ENV_FILE
echo "LIBRARIES_DIR=$LIBRARIES_DIR" >> $GENERATED_PATHS_ENV_FILE
echo "STATIC_FILES_DIR=$STATIC_FILES_DIR" >> $GENERATED_PATHS_ENV_FILE
echo "LOG_DIR=$LOG_DIR" >> $GENERATED_PATHS_ENV_FILE
echo "TMP_UPLOADED_FILES_DIR=$TMP_UPLOADED_FILES_DIR" >> $GENERATED_PATHS_ENV_FILE