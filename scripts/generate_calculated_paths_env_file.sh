#!/bin/bash

load_env_vars () {
    echo "Loading environment variables..."
    check_vars_are_set "LIBRARIES_DIR_NAME"

    REQUIRED_BOOL_VARS=(
        "APP_IS_EXPOSED"
        "STATIC_FILES_ARE_NEEDED"
        "DJANGO_LOGS_ARE_NEEDED"
        "AUDIO_META_ANALYSE_IS_NEEDED"
    )
    check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}
    echo "Environment variables loaded successfully."
}

echo "Generating the env file with calculated paths..."

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
GENERATED_PATHS_ENV_FILE="${PROJECT_DIR}env/calculated_paths/.env"

source ${SCRIPTS_DIR}utils.sh
load_env_vars

[ -f "$GENERATED_PATHS_ENV_FILE" ] && rm -f "$GENERATED_PATHS_ENV_FILE"
output=$(touch "$GENERATED_PATHS_ENV_FILE")
if [ $? -ne 0 ]; then
    echo "Failed to create the generated paths env file: $output" >&2
    exit 1
fi

if [ "$APP_IS_EXPOSED" = "true" ]; then
    check_vars_are_set "MEDIA_DIR"
    check_vars_are_set "TMP_UPLOADED_FILES"
    if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "STATIC_FILES"
    fi
    if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "DJANGO_LOG_DIR"
        DJANGO_LOG_DIR="${PROJECT_DIR}${DJANGO_LOG_DIR}"
    fi
else
    check_vars_are_set "MEDIA_DEFAULT_INTERNAL_DIR"
    MEDIA_DIR="${PROJECT_DIR}${MEDIA_DEFAULT_INTERNAL_DIR}"
    if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "STATIC_FILES_DEFAULT_INTERNAL_DIR"
        STATIC_FILES="${PROJECT_DIR}${STATIC_FILES_DEFAULT_INTERNAL_DIR}"
    fi
    if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "DJANGO_LOG_DEFAULT_INTERNAL_DIR"
        DJANGO_LOG_DIR="${PROJECT_DIR}${DJANGO_LOG_DEFAULT_INTERNAL_DIR}"
    fi
    if [ "$AUDIO_META_ANALYSE_IS_NEEDED" = "true" ]; then
        check_vars_are_set "TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR"
        TMP_UPLOADED_FILES="${PROJECT_DIR}${TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR}"
    fi
fi

LIBRARIES_DIR="${MEDIA_DIR}${LIBRARIES_DIR_NAME}/"

echo "MEDIA_DIR=$MEDIA_DIR" >> "$GENERATED_PATHS_ENV_FILE"
echo "LIBRARIES_DIR_NAME=$LIBRARIES_DIR_NAME" >> "$GENERATED_PATHS_ENV_FILE"
echo "LIBRARIES_DIR=$LIBRARIES_DIR" >> "$GENERATED_PATHS_ENV_FILE"
echo "TMP_UPLOADED_FILES=$TMP_UPLOADED_FILES" >> "$GENERATED_PATHS_ENV_FILE"

if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
    echo "STATIC_FILES=$STATIC_FILES" >> "$GENERATED_PATHS_ENV_FILE"
else
    echo "STATIC_FILES_ARE_NEEDED is set to false so STATIC_FILES is not set."
fi

if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
    check_vars_are_set "DJANGO_LOG_DIR"
    echo "DJANGO_LOG_DIR=$DJANGO_LOG_DIR" >> "$GENERATED_PATHS_ENV_FILE"
fi


echo "Generated the env file with calculated paths successfully."