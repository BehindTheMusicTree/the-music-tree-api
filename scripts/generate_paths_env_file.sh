#!/bin/bash

GENERATED_PATHS_ENV_FILE=$1

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
ENV_PATH="$SCRIPT_DIR../env/.env"
DEFAULT_INTERNAL_PATHS_CONFIG_FILE="$SCRIPT_DIR../default_internal_paths_settings.json"

if [ -f "$ENV_PATH" ]; then
    echo "Loading environment variables from ${ENV_PATH}"
    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$ENV_PATH"
else
    echo "$ENV_PATH env file does not exist"
fi

if [ -z $EXTERNAL_DIRS_NEEDED ]; then
    echo "EXTERNAL_DIRS_NEEDED is not set."
    exit 1
fi

if $EXTERNAL_DIRS_NEEDED; then
    echo "EXTERNAL_DIRS_NEEDED is set to true"
    if [ -z $MEDIA_DIR ]; then
        echo "MEDIA_DIR is not set"
        exit 1
    fi

    if [ -z $LIBRARIES_DIR_NAME ]; then
        echo "LIBRARIES_DIR_NAME is not set"
        exit 1
    fi

    if [ -z $STATIC_FILES_DIR ]; then
        echo "STATIC_FILES_DIR is not set"
        exit 1
    fi

    if [ -z $DJANGO_LOG_DIR ]; then
        echo "DJANGO_LOG_DIR is not set"
        exit 1
    fi

    if [ -z $TMP_UPLOADED_FILES_DIR ]; then
        echo "TMP_UPLOADED_FILES_DIR is not set"
        exit 1
    fi
else
    echo "EXTERNAL_DIRS_NEEDED is set to false"
    if [ ! -f "$DEFAULT_INTERNAL_PATHS_CONFIG_FILE" ]; then
        echo "The default internal paths configuration file '${DEFAULT_INTERNAL_PATHS_CONFIG_FILE}' was not found."
        exit 1
    else
        echo "Loading the default internal paths configuration values from ${DEFAULT_INTERNAL_PATHS_CONFIG_FILE}"
    fi

    config=$(cat "$DEFAULT_INTERNAL_PATHS_CONFIG_FILE")
    MEDIA_DIR=$(echo "$config" | jq -r '.["media"]')
    LIBRARIES_DIR_NAME=$(echo "$config" | jq -r '.["librariesDirName"]')
    STATIC_FILES_DIR=$(echo "$config" | jq -r '.["staticFiles"]')
    LOG_DIR=$(echo "$config" | jq -r '.["log"]')
    TMP_UPLOADED_FILES_DIR=$(echo "$config" | jq -r '.["tmpUploadedFiles"]')
fi

LIBRARIES_DIR=${MEDIA_DIR}${LIBRARIES_DIR_NAME}

echo "MEDIA_DIR: $MEDIA_DIR"
echo "LIBRARIES_DIR: $LIBRARIES_DIR"
echo "STATIC_FILES_DIR: $STATIC_FILES_DIR"
echo "LOG_DIR: $LOG_DIR"
echo "TMP_UPLOADED_FILES_DIR: $TMP_UPLOADED_FILES_DIR"

if [ -f $GENERATED_PATHS_ENV_FILE ]; then
    rm -f $GENERATED_PATHS_ENV_FILE
fi
touch $GENERATED_PATHS_ENV_FILE
echo "MEDIA_DIR=$MEDIA_DIR" >> $GENERATED_PATHS_ENV_FILE
echo "LIBRARIES_DIR=${LIBRARIES_DIR}" >> $GENERATED_PATHS_ENV_FILE
echo "STATIC_FILES_DIR=${STATIC_FILES_DIR}" >> $GENERATED_PATHS_ENV_FILE
echo "LOG_DIR=${LOG_DIR}" >> $GENERATED_PATHS_ENV_FILE
echo "TMP_UPLOADED_FILES_DIR=${TMP_UPLOADED_FILES_DIR}" >> $GENERATED_PATHS_ENV_FILE
