#!/bin/bash

create_directory_if_not_exists() {
    local dir_path=$1
    if [ ! -d "$dir_path" ]; then
        echo "Creating directory $dir_path"
        OUTPUT=$(mkdir -p "$dir_path")
        if [ $? -ne 0 ]; then
            echo "Failed to create directory $dir_path. Details: $OUTPUT" >&2
            exit 1
        fi
        
    else
        echo "Directory $dir_path already exists"
    fi
}

touch_file_or_exit() {
    local file_path=$1
    OUTPUT=$(touch "$file_path")
    if [ $? -ne 0 ]; then
        echo "Failed to create file $file_path. Details: $OUTPUT" >&2
        exit 1
    fi
}

set_read_write_permissions_and_owner() {
    local path=$1
    local user=$(whoami)
    OUTPUT=$(chmod -R 740 "$path")
    if [ $? -ne 0 ]; then
        echo "Failed to change permissions of $path. Details: $OUTPUT" >&2
        exit 1
    fi
    OUTPUT=$(chown -R "$user" "$path")
    if [ $? -ne 0 ]; then
        echo "Failed to change owner of $path. Details: $OUTPUT" >&2
        exit 1
    fi
}

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
ENV_FILE=${PROJECT_DIR}env/.env
source "${SCRIPTS_DIR}utils.sh"

load_project_env_file

REQUIRED_BOOL_VARS=(
  "APP_IS_EXPOSED"
  "DJANGO_LOGS_ARE_NEEDED"
  "STATIC_FILES_ARE_NEEDED"
  "AUDIO_META_ANALYSE_IS_NEEDED"
)
check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}

load_project_calculated_paths_env_vars

create_directory_if_not_exists "$LIBRARIES_DIR"

if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
    create_directory_if_not_exists "$STATIC_FILES_DIR"
    check_vars_are_set "STATIC_FILES_DEFAULT_INTERNAL_DIR"

    DEFAULT_STATIC_FILES_DIR="${PROJECT_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR"
    if [ "$STATIC_FILES_DIR" != "$DEFAULT_STATIC_FILES_DIR" ]; then
        echo "STATIC_FILES_DIR is not the default internal directory. Moving static files to $STATIC_FILES_DIR"
        if [ ! -d "$DEFAULT_STATIC_FILES_DIR" ] || [ "$(find "$DEFAULT_STATIC_FILES_DIR" -mindepth 1 -print -quit | grep -q .)" ]; then
            echo "No static files found in default internal directory $STATIC_FILES_DEFAULT_INTERNAL_DIR"
        else
            OUTPUT=$(mv "$DEFAULT_STATIC_FILES_DIR"/* "$STATIC_FILES_DIR")
            if [ $? -ne 0 ]; then
                echo "Failed to move static files from default internal directory to $STATIC_FILES_DIR. Details: $OUTPUT" >&2
                exit 1
            fi
            echo "Deleting default internal static files directory"
            OUTPUT=$(rm -rf "$DEFAULT_STATIC_FILES_DIR")
            if [ $? -ne 0 ]; then
                echo "Failed to delete default internal static files directory. Details: $OUTPUT" >&2
                exit 1
            fi
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
        check_vars_are_set "$log_filename"
        touch_file_or_exit "${DJANGO_LOG_DIR}${!log_filename}"
    done
    set_read_write_permissions_and_owner "$DJANGO_LOG_DIR"
else
    echo "DJANGO_LOGS_ARE_NEEDED is set to false. Django logs are not needed."
fi

if [ "$APP_IS_EXPOSED" = "true" ]; then
    REQUIRED_NON_BOOL_VARS=(
        GUNICORN_LOG_DIR
        GUNICORN_LOG_ERROR_FILENAME
        GUNICORN_LOG_ACCESS_FILENAME
    )
    for var_name in "${REQUIRED_NON_BOOL_VARS[@]}"; do
        check_vars_are_set "$var_name"
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
    create_directory_if_not_exists "$TMP_UPLOADED_FILES"
    set_read_write_permissions_and_owner "$TMP_UPLOADED_FILES"
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

echo "Make all scripts in $SCRIPTS_DIR executable."
for script in "${SCRIPTS_DIR}"*; do
    if [ -f "$script" ]; then
        chmod +x "$script"
    fi
done

echo "All directories and files are created and permissions are set."