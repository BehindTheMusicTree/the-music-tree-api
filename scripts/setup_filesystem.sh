#!/bin/bash

set -e

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

check_bool_var() {
    local var_name="$1"
    local var_value="${!1}"
    check_var_is_set "$var_name"
    var_value_lower=$(echo "$var_value" | tr '[:upper:]' '[:lower:]')
    if [ "$var_value_lower" != "true" ] && [ "$var_value_lower" != "false" ]; then
        print_error_and_exit "$var_name must be 'true' or 'false'"
    fi
}

create_directory_if_not_exists() {
    local dir_path=$1
    if [ ! -d "$dir_path" ]; then
        echo "Creating directory $dir_path"
        mkdir -p "$dir_path" || print_error_and_exit "Failed to create directory $dir_path"
    else
        echo "Directory $dir_path already exists"
    fi
}

touch_file_or_exit() {
    local file_path=$1
    touch "$file_path" || print_error_and_exit "Failed to create file $file_path"
}

set_read_write_permissions_and_owner() {
    local path=$1
    local user=$(whoami)
    chmod -R 740 "$path" || print_error_and_exit "Failed to change permissions of $path"
    chown -R "$user" "$path" || print_error_and_exit "Failed to change owner of $path"
}

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
ENV_FILE=${PROJECT_DIR}env/.env

if [ ! -f "$ENV_FILE" ]; then
    echo "Env file $ENV_FILE does not exist" >&2
else
    echo "Loading environment variables from ${ENV_FILE}"
    while IFS='=' read -r key value; do
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$ENV_FILE"
fi

BOOL_VARS=(
  "APP_IS_EXPOSED"
  "DJANGO_LOGS_ARE_NEEDED"
  "STATIC_FILES_ARE_NEEDED"
  "AUDIO_META_ANALYSE_IS_NEEDED"
)
for VAR in "${BOOL_VARS[@]}"; do
  check_bool_var "$VAR"
done

REQUIRED_VARS=(
  "LIBRARIES_DIR_NAME"
  "MEDIA_DEFAULT_INTERNAL_DIR"
)
for VAR in "${REQUIRED_VARS[@]}"; do
  check_var_is_set "$VAR"
done

CALCULATED_PATHS_ENV_FILE="${PROJECT_DIR}env/calculated_paths/.env"
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    print_error_and_exit "Failed to generate calculated paths env file"
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value; do
    export "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

create_directory_if_not_exists "$LIBRARIES_DIR"

if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
    create_directory_if_not_exists "$STATIC_FILES_DIR"
    check_var_is_set "STATIC_FILES_DEFAULT_INTERNAL_DIR"

    DEFAULT_STATIC_FILES_DIR="${PROJECT_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR"
    if [ "$STATIC_FILES_DIR" != "$DEFAULT_STATIC_FILES_DIR" ]; then
        echo "STATIC_FILES_DIR is not the default internal directory. Moving static files to $STATIC_FILES_DIR"
        if [ ! -d "$DEFAULT_STATIC_FILES_DIR" ] || [ "$(find "$DEFAULT_STATIC_FILES_DIR" -mindepth 1 -print -quit | grep -q .)" ]; then
            echo "No static files found in default internal directory $STATIC_FILES_DEFAULT_INTERNAL_DIR"
        else
            mv "$DEFAULT_STATIC_FILES_DIR"/* "$STATIC_FILES_DIR" || print_error_and_exit "Failed to move static files to $STATIC_FILES_DIR"
            echo "Deleting default internal static files directory"
            rm -r "$DEFAULT_STATIC_FILES_DIR" || print_error_and_exit "Failed to delete default internal static files directory"
        fi
    else
        echo "STATIC_FILES_DIR is the default internal directory $DEFAULT_STATIC_FILES_DIR"
    fi
    set_read_write_permissions_and_owner "$STATIC_FILES_DIR"
fi

if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
    echo "DJANGO_LOGS_ARE_NEEDED is set to true. Creating Django log directories."
    create_directory_if_not_exists "$DJANGO_LOG_DIR"

    log_filenames=(
        DJANGO_LOG_GENERAL_FILENAME
        DJANGO_LOG_INFO_FILENAME
        DJANGO_LOG_REQUESTS_FILENAME
        DJANGO_LOG_REQUESTS_DEBUG_FILENAME
        DJANGO_LOG_EXCEPTIONS_FILENAME
        DJANGO_LOG_DJANGO_FILENAME
        DJANGO_LOG_APP_FILENAME
    )
    for log_filename in "${log_filenames[@]}"; do
        check_var_is_set "$log_filename"
        touch_file_or_exit "${DJANGO_LOG_DIR}${!log_filename}"
    done
    set_read_write_permissions_and_owner "$DJANGO_LOG_DIR"
else
    echo "DJANGO_LOGS_ARE_NEEDED is set to false. Django logs are not needed."
fi

if [ "$APP_IS_EXPOSED" = "true" ]; then
    required_vars=(
        GUNICORN_LOG_DIR
        GUNICORN_LOG_ERROR_FILENAME
        GUNICORN_LOG_ACCESS_FILENAME
    )
    for var_name in "${required_vars[@]}"; do
        check_var_is_set "$var_name"
    done

    GUNICORN_LOG_ERROR_FILE="${GUNICORN_LOG_DIR}${GUNICORN_LOG_ERROR_FILENAME}"
    GUNICORN_LOG_ACCESS_FILE="${GUNICORN_LOG_DIR}${GUNICORN_LOG_ACCESS_FILENAME}"
    create_directory_if_not_exists "$GUNICORN_LOG_DIR"
    touch_file_or_exit "$GUNICORN_LOG_ERROR_FILE"
    touch_file_or_exit "$GUNICORN_LOG_ACCESS_FILE"
    set_read_write_permissions_and_owner "$GUNICORN_LOG_DIR"
else
    echo "APP_IS_EXPOSED is set to false. Gunicorn logs are not needed."
fi

if [ "$AUDIO_META_ANALYSE_IS_NEEDED" = "true" ]; then
    create_directory_if_not_exists "$TMP_UPLOADED_FILES_DIR"
    set_read_write_permissions_and_owner "$TMP_UPLOADED_FILES_DIR"
else
    echo "AUDIO_META_ANALYSE_IS_NEEDED is set to false. Temp uploaded files dir is not needed."
fi

if [ -z "$MEDIA_DIR" ]; then
    echo "MEDIA_DIR is not set. Using default internal directory."
    MEDIA_DIR="${PROJECT_DIR}media/"
fi
echo "MEDIA_DIR is set to $MEDIA_DIR"
create_directory_if_not_exists "$MEDIA_DIR"
set_read_write_permissions_and_owner "$MEDIA_DIR"

check_var_is_set "INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT_NAME"
chmod +x ${SCRIPTS_DIR}${INIT_IF_NECESSARY_DB_AND_ROLE_SCRIPT_NAME}