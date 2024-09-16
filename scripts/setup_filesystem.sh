#!/bin/bash

load_env_vars () {
    load_project_env_file_if_exists
    local REQUIRED_BOOL_VARS=(
        "APP_IS_EXPOSED"
        "DJANGO_LOGS_ARE_NEEDED"
        "STATIC_FILES_ARE_NEEDED"
        "AUDIO_META_ANALYSE_IS_NEEDED"
    )
    check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}
    load_project_calculated_paths_env_vars
}

setup_static_files () {
    if [ "$STATIC_FILES_ARE_NEEDED" = "true" ]; then
        echo "STATIC_FILES_ARE_NEEDED is set to true. Setting up static files..."
        create_directory_if_not_exists_or_exit "$STATIC_FILES"
        check_vars_are_set "STATIC_FILES_DEFAULT_INTERNAL_DIR"

        local DEFAULT_STATIC_FILES="${PROJECT_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR"
        if [ "$STATIC_FILES" != "$DEFAULT_STATIC_FILES" ]; then
            echo "STATIC_FILES: $STATIC_FILES"
            echo "DEFAULT_STATIC_FILES: $DEFAULT_STATIC_FILES"
            echo "STATIC_FILES is not the default internal directory. Moving static files to $STATIC_FILES"
            if [ ! -d "$DEFAULT_STATIC_FILES" ] || [ "$(find "$DEFAULT_STATIC_FILES" -mindepth 1 -print -quit | grep -q .)" ]; then
                echo "No static files found in default internal directory $STATIC_FILES_DEFAULT_INTERNAL_DIR ."
            else
                local output=$(mv "$DEFAULT_STATIC_FILES"* "$STATIC_FILES")
                if [ $? -ne 0 ]; then
                    echo "Failed to move static files from default internal directory to $STATIC_FILES: $output" >&2
                    exit 1
                fi
                echo "Deleting default internal static files directory"
                output=$(rm -rf "$DEFAULT_STATIC_FILES")
                if [ $? -ne 0 ]; then
                    echo "Failed to delete default internal static files directory: $output" >&2
                    exit 1
                fi
            fi
        else
            echo "STATIC_FILES is the default internal directory $DEFAULT_STATIC_FILES"
        fi
        set_read_write_permissions_and_owner_or_exit "$STATIC_FILES"
        echo "Static files are set up."
    else
        echo "STATIC_FILES_ARE_NEEDED is set to false. Static files are not needed."
    fi
}

setup_django_log () {
    if [ "$DJANGO_LOGS_ARE_NEEDED" = "true" ]; then
        echo "DJANGO_LOGS_ARE_NEEDED is set to true. Creating Django log directories."
        create_directory_if_not_exists_or_exit "$DJANGO_LOG_DIR"

        local LOG_FILENAMES=(
            DJANGO_LOG_GENERAL_FILENAME
            DJANGO_LOG_INFO_FILENAME
            DJANGO_LOG_REQUESTS_FILENAME
            DJANGO_LOG_REQUESTS_DEBUG_FILENAME
            DJANGO_LOG_EXCEPTIONS_FILENAME
            DJANGO_LOG_DJANGO_FILENAME
            DJANGO_LOG_APP_FILENAME
        )
        for log_filename in "${LOG_FILENAMES[@]}"; do
            check_vars_are_set "$log_filename"
            touch_file_or_exit "${DJANGO_LOG_DIR}${!log_filename}"
        done
        set_read_write_permissions_and_owner_or_exit "$DJANGO_LOG_DIR"
    else
        echo "DJANGO_LOGS_ARE_NEEDED is set to false. Django logs are not needed."
    fi
}

setup_gunicorn_log () {
    if [ "$APP_IS_EXPOSED" = "true" ]; then
        echo "App is exposed. Setting up Gunicorn logs."
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
        create_directory_if_not_exists_or_exit "$GUNICORN_LOG_DIR"
        touch_file_or_exit "$GUNICORN_LOG_ERROR_FILE"
        touch_file_or_exit "$GUNICORN_LOG_ACCESS_FILE"
        set_read_write_permissions_and_owner_or_exit "$GUNICORN_LOG_DIR"
        echo "Gunicorn logs are set up."
    else
        echo "APP_IS_EXPOSED is set to false. Gunicorn logs are not needed."
    fi
}

setup_media_dirs () {
    echo "Setting up media directories..."
    if [ "$AUDIO_META_ANALYSE_IS_NEEDED" = "true" ]; then
        create_directory_if_not_exists_or_exit "$TMP_UPLOADED_FILES"
        set_read_write_permissions_and_owner_or_exit "$TMP_UPLOADED_FILES"
    else
        echo "AUDIO_META_ANALYSE_IS_NEEDED is set to false. Temp uploaded files dir is not needed."
    fi

    if [ -z "$MEDIA_DIR" ]; then
        echo "MEDIA_DIR is not set. Using default internal directory."
        MEDIA_DIR="${PROJECT_DIR}media/"
    fi
    echo "MEDIA_DIR is set to $MEDIA_DIR"
    create_directory_if_not_exists_or_exit "$MEDIA_DIR"
    set_read_write_permissions_and_owner_or_exit "$MEDIA_DIR"
    echo "Media directories are set up."
}

echo "Setting up filesystem..."

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
source "${SCRIPTS_DIR}utils.sh"

load_env_vars

create_directory_if_not_exists_or_exit "$LIBRARIES_DIR"

setup_static_files
setup_django_log
setup_gunicorn_log
setup_media_dirs

echo "Making all scripts in $SCRIPTS_DIR executable..."
for script in "${SCRIPTS_DIR}"*; do
    if [ -f "$script" ]; then
        output=$(chmod +x "$script")
        if [ $? -ne 0 ]; then
            echo "Failed to make $script executable: $output" >&2
            exit 1
        fi
    fi
done
echo "All scripts in $SCRIPTS_DIR are now executable."

echo "All directories and files are created and permissions are set."