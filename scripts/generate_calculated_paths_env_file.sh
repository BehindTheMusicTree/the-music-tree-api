#!/bin/bash

print_error_and_exit() {
    echo "Error: $1" >&2
    exit 1
}

check_var_is_set() {
    local VAR_NAME=$1
    if [ -z "${!VAR_NAME}" ]; then
        print_error_and_exit "$VAR_NAME is not set"
    fi
}

echo "Generating the env file with calculated paths and db host"

[ -z "$1" ] && print_error_and_exit "NO BASE DIR PROVIDED."
BASE_DIR=$1

[ -z "$2" ] && print_error_and_exit "NO CALCULATED PATHS ENV FILE PATH PROVIDED."
GENERATED_PATHS_ENV_FILE=$2

REQUIRED_VARS=( \
    "APP_IS_EXPOSED" \
    "LIBRARIES_DIR_NAME" \
    "DB_IS_NEEDED" "STATIC_FILES_ARE_NEEDED" \
    "DJANGO_LOGS_ARE_NEEDED" \
    "AUDIO_META_ANALYSE_IS_NEEDED")
for VAR in "${REQUIRED_VARS[@]}"; do
    check_var_is_set "$VAR"
done

if [ "$APP_IS_EXPOSED" = "true" ]; then
    echo "APP_IS_EXPOSED is set to true"
    check_var_is_set "MEDIA_DIR"
    check_var_is_set "TMP_UPLOADED_FILES_DIR"
    if [ "$DB_IS_NEEDED" = "true" ]; then
        check_var_is_set "DB_CONTAINER_NAME"
        DB_HOST=$DB_CONTAINER_NAME
    fi
    if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
        check_var_is_set "STATIC_FILES_DIR"
        STATIC_FILES_DIR="${BASE_DIR}${STATIC_FILES_DIR}"
    fi
    if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
        check_var_is_set "DJANGO_LOG_DIR"
        DJANGO_LOG_DIR="${BASE_DIR}${DJANGO_LOG_DIR}"
    fi
else
    echo "APP_IS_EXPOSED is set to false"
    check_var_is_set "MEDIA_DEFAULT_INTERNAL_DIR"
    MEDIA_DIR="${BASE_DIR}${MEDIA_DEFAULT_INTERNAL_DIR}"
    if [ "$DB_IS_NEEDED" = "true" ]; then
        check_var_is_set "DB_HOST"
    fi
    if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
        check_var_is_set "STATIC_FILES_DEFAULT_INTERNAL_DIR"
        STATIC_FILES_DIR="${BASE_DIR}${STATIC_FILES_DEFAULT_INTERNAL_DIR}"
    fi
    if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
        check_var_is_set "DJANGO_LOG_DEFAULT_INTERNAL_DIR"
        DJANGO_LOG_DIR="${BASE_DIR}${DJANGO_LOG_DEFAULT_INTERNAL_DIR}"
    fi
    if [ "$AUDIO_META_ANALYSE_IS_NEEDED" = "true" ]; then
        check_var_is_set "TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR"
        TMP_UPLOADED_FILES_DIR="${BASE_DIR}${TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR}"
    fi
fi

LIBRARIES_DIR="${MEDIA_DIR}${LIBRARIES_DIR_NAME}/"

[ -f "$GENERATED_PATHS_ENV_FILE" ] && rm -f "$GENERATED_PATHS_ENV_FILE"
touch "$GENERATED_PATHS_ENV_FILE"

echo "MEDIA_DIR: $MEDIA_DIR"
echo "LIBRARIES_DIR_NAME: $LIBRARIES_DIR_NAME"
echo "LIBRARIES_DIR: $LIBRARIES_DIR"

echo "MEDIA_DIR=$MEDIA_DIR" >> "$GENERATED_PATHS_ENV_FILE"
echo "LIBRARIES_DIR_NAME=$LIBRARIES_DIR_NAME" >> "$GENERATED_PATHS_ENV_FILE"
echo "LIBRARIES_DIR=$LIBRARIES_DIR" >> "$GENERATED_PATHS_ENV_FILE"

echo "DB_HOST=$DB_HOST" >> "$GENERATED_PATHS_ENV_FILE"

if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
    echo "STATIC_FILES_DIR: $STATIC_FILES_DIR"
    echo "STATIC_FILES_DIR=$STATIC_FILES_DIR" >> "$GENERATED_PATHS_ENV_FILE"
else
    echo "STATIC_FILES_ARE_NEEDED is set to false so STATIC_FILES_DIR is not set"
fi

if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
    check_var_is_set "DJANGO_LOG_DIR"
    echo "DJANGO_LOG_DIR: $DJANGO_LOG_DIR"
    echo "DJANGO_LOG_DIR=$DJANGO_LOG_DIR" >> "$GENERATED_PATHS_ENV_FILE"
else
    echo "DJANGO_LOGS_ARE_NEEDED is set to false so DJANGO_LOG_DIR is not set"
fi

echo "TMP_UPLOADED_FILES_DIR: $TMP_UPLOADED_FILES_DIR"
echo "TMP_UPLOADED_FILES_DIR=$TMP_UPLOADED_FILES_DIR" >> "$GENERATED_PATHS_ENV_FILE"