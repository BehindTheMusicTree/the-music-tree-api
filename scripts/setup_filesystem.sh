#!/bin/bash

load_env_vars () {
    echo "Loading environment variables for the filesystem setup..."
    load_app_env_file_if_exists
    check_bool_vars_are_set "APP_IS_EXPOSED"
    load_project_calculated_paths_env_vars
    echo "Environment variables loaded for the filesystem setup."
}

setup_static_files () {
    if [ -n "$STATIC_FILES_INTERNAL" ]; then
        echo "STATIC_FILES_INTERNAL is set. Static files are needed."
        create_directory_if_not_exists_or_exit "$STATIC_FILES_DEFAULT"

        if [ "$STATIC_FILES" != "$STATIC_FILES_DEFAULT" ]; then
            echo "STATIC_FILES ${STATIC_FILES} is not the default internal directory ${STATIC_FILES_DEFAULT} . "\
                "Setting up $STATIC_FILES ..."
            create_directory_if_not_exists_or_exit "$STATIC_FILES"
          
            if [ ! -d "$STATIC_FILES_DEFAULT" ] || [ "$(find "$STATIC_FILES_DEFAULT" -mindepth 1 -print -quit | grep -q .)" ]; then
                echo "No static files found in default internal directory $STATIC_FILES_DEFAULT ."
            else
                echo "Moving static files from default internal directory to $STATIC_FILES ..."  
                local output=$(mv "$STATIC_FILES_DEFAULT"* "$STATIC_FILES")
                if [ $? -ne 0 ]; then
                    echo "Failed to move static files from ${STATIC_FILES_DEFAULT} directory to $STATIC_FILES: $output" >&2
                    exit 1
                fi
                echo "Static files moved successfully."

                echo "Deleting default internal static files directory..."
                output=$(rm -rf "$STATIC_FILES_DEFAULT")
                if [ $? -ne 0 ]; then
                    echo "Failed to delete default internal static files directory: $output" >&2
                    exit 1
                fi
                echo "Default internal static files directory deleted successfully."

            fi
        else
            echo "STATIC_FILES is the default internal directory $STATIC_FILES_DEFAULT"
        fi
        set_read_write_permissions_and_owner_or_exit "$STATIC_FILES"
        echo "Static files are set up."
    else
        echo "STATIC_FILES_INTERNAL is not set. Static files are not needed."
    fi
}

setup_django_log () {
    if [ -n "$DJANGO_LOGS_DIR" ]; then
        echo "DJANGO_LOGS_DIR is set. Setting Django logs dirextories and files."
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
        echo "DJANGO_LOGS_DIR is not set. Django logs are not needed."
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
    if [ -n "${TMP_UPLOADED_FILES}" ]; then
        echo "TMP_UPLOADED_FILES is set. Setting up temp uploaded files directory and media direcroties..."
        create_directory_if_not_exists_or_exit "$TMP_UPLOADED_FILES"
        set_read_write_permissions_and_owner_or_exit "$TMP_UPLOADED_FILES"
        echo "Temp uploaded files directory is set up."

        echo "Setting up media directory..."
        create_directory_if_not_exists_or_exit "$MEDIA_DIR"
        create_directory_if_not_exists_or_exit "$LIBRARIES_DIR"
        set_read_write_permissions_and_owner_or_exit "$MEDIA_DIR"
        echo "Media directories are set up."
    else
        echo "TMP_UPLOADED_FILES is not set. The app will not handle media files."
    fi
}

echo "Setting up filesystem..."

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
APP_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
source "${SCRIPTS_DIR}utils.sh"

load_env_vars

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

echo "The filesystem is set up."