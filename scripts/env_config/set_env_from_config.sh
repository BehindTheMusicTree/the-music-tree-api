#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source "${SCRIPT_DIR}load_env_config.sh"

if [ -z $ENV ]; then
    echo "ENV is not set"
    exit 1
fi
echo "ENV is set to $ENV"

if [ -z $EXTERNAL_DIRS_NEEDED ]; then
    echo "EXTERNAL_DIRS_NEEDED is not set"
    exit 1
fi

if [ $EXTERNAL_DIRS_NEEDED = "true" ]; then
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
    export MEDIA_DIR=${PROJECT_DIR}$MEDIA_DEFAULT_INTERNAL_DIR
    export LIBRARIES_DIR_NAME=${PROJECT_DIR}$LIBRARIES_DEFAULT_INTERNAL_DIR_NAME
    export STATIC_FILES_DIR=${PROJECT_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR
    export LOG_DIR=${PROJECT_DIR}$LOG_DEFAULT_INTERNAL_DIR
    export TMP_UPLOADED_FILES_DIR=${PROJECT_DIR}$TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR
fi

export LIBRARIES_DIR=${MEDIA_DIR}${LIBRARIES_DIR_NAME}