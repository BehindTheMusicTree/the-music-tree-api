#!/bin/bash

print_error_and_exit() {
    echo "Error: $1" >&2
    exit 1
}

check_var_is_set() {
    local var_name=$1
    if [ -z "${!var_name}" ]; then
        print_error_and_exit "$var_name is not set"
    fi
}

echo "Generating calculated paths env file"

[ -z "$1" ] && print_error_and_exit "no base dir provided."
BASE_DIR=$1

[ -z "$2" ] && print_error_and_exit "no calculated paths env file path provided."
GENERATED_PATHS_ENV_FILE=$2

required_vars=("APP_IS_EXPOSED" "LIBRARIES_DIR_NAME")
for var in "${required_vars[@]}"; do
    check_var_is_set "$var"
done

if [ "$APP_IS_EXPOSED" = "true" ]; then
    echo "APP_IS_EXPOSED is set to true"
    required_vars=("MEDIA_DIR" "TMP_UPLOADED_FILES_DIR")
    [ "$STATIC_FILES_ARE_NEEDED" = "true" ] && required_vars+=("STATIC_FILES_DIR")
    [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ] && required_vars+=("DJANGO_LOG_DIR")
    for var in "${required_vars[@]}"; do
        check_var_is_set "$var"
    done
else
    echo "APP_IS_EXPOSED is set to false"
    MEDIA_DIR="${BASE_DIR}${MEDIA_DEFAULT_INTERNAL_DIR}"
    [ "$STATIC_FILES_ARE_NEEDED" = "true" ] && STATIC_FILES_DIR="${BASE_DIR}${STATIC_FILES_DEFAULT_INTERNAL_DIR}"
    [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ] && DJANGO_LOG_DIR="${BASE_DIR}${DJANGO_LOG_DEFAULT_INTERNAL_DIR}"
    TMP_UPLOADED_FILES_DIR="${BASE_DIR}${TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR}"
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