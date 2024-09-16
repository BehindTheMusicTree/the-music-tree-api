#!/bin/bash

echo "Generating the env file with calculated paths..."

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
GENERATED_PATHS_ENV_FILE="${PROJECT_DIR}env/calculated_paths/.env"

source ${SCRIPTS_DIR}utils.sh

check_vars_are_set "LIBRARIES_DIR_NAME"

REQUIRED_BOOL_VARS=(
    "APP_IS_EXPOSED"
    "STATIC_FILES_ARE_NEEDED"
    "DJANGO_LOGS_ARE_NEEDED"
    "AUDIO_META_ANALYSE_IS_NEEDED"
)
check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}

if [ "$APP_IS_EXPOSED" = "true" ]; then
    check_vars_are_set "MEDIA_DIR"
    check_vars_are_set "TMP_UPLOADED_FILES"
    if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "STATIC_FILES"
        STATIC_FILES="${BASE_DIR}${STATIC_FILES}"
    fi
    if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "DJANGO_LOG_DIR"
        DJANGO_LOG_DIR="${BASE_DIR}${DJANGO_LOG_DIR}"
    fi
else
    check_vars_are_set "MEDIA_DEFAULT_INTERNAL_DIR"
    MEDIA_DIR="${BASE_DIR}${MEDIA_DEFAULT_INTERNAL_DIR}"
    if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "STATIC_FILES_DEFAULT_INTERNAL_DIR"
        STATIC_FILES="${BASE_DIR}${STATIC_FILES_DEFAULT_INTERNAL_DIR}"
    fi
    if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
        check_vars_are_set "DJANGO_LOG_DEFAULT_INTERNAL_DIR"
        DJANGO_LOG_DIR="${BASE_DIR}${DJANGO_LOG_DEFAULT_INTERNAL_DIR}"
    fi
    if [ "$AUDIO_META_ANALYSE_IS_NEEDED" = "true" ]; then
        check_vars_are_set "TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR"
        TMP_UPLOADED_FILES="${BASE_DIR}${TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR}"
    fi
fi

LIBRARIES_DIR="${MEDIA_DIR}${LIBRARIES_DIR_NAME}/"

[ -f "$GENERATED_PATHS_ENV_FILE" ] && rm -f "$GENERATED_PATHS_ENV_FILE"
output=$(touch "$GENERATED_PATHS_ENV_FILE")
if [ $? -ne 0 ]; then
    echo "Failed to create the generated paths env file: $output" >&2
    exit 1
fi

echo "MEDIA_DIR=$MEDIA_DIR" >> "$GENERATED_PATHS_ENV_FILE"
echo "LIBRARIES_DIR_NAME=$LIBRARIES_DIR_NAME" >> "$GENERATED_PATHS_ENV_FILE"
echo "LIBRARIES_DIR=$LIBRARIES_DIR" >> "$GENERATED_PATHS_ENV_FILE"

if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
    echo "STATIC_FILES=$STATIC_FILES" >> "$GENERATED_PATHS_ENV_FILE"
else
    echo "STATIC_FILES_ARE_NEEDED is set to false so STATIC_FILES is not set."
fi

if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
    check_vars_are_set "DJANGO_LOG_DIR"
    echo "DJANGO_LOG_DIR=$DJANGO_LOG_DIR" >> "$GENERATED_PATHS_ENV_FILE"
fi

echo "TMP_UPLOADED_FILES=$TMP_UPLOADED_FILES" >> "$GENERATED_PATHS_ENV_FILE"

echo "Generated the env file with calculated paths successfully."