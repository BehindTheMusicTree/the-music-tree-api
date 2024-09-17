#!/bin/bash

load_env_vars () {
    echo "Loading environment variables for the filesystem setup..."
    load_app_env_file_if_exists
    check_vars_are_set ENV
    check_bool_vars_are_set APP_IS_EXPOSED
    load_project_calculated_paths_env_vars
    echo "Environment variables loaded for the filesystem setup."
}

setup_static_files () {
    if [ $ENV = "COLLECT_STATIC" ]; then
        check_vars_are_set STATIC_FILES_DEFAULT
        echo "ENV is set to COLLECT_STATIC. Setting up the filesystem..."
        if [ -n "$STATIC_FILES_DIR_EXTERNAL" ]; then
            echo "In collct static mode, $STATIC_FILES_DIR_EXTERNAL must not be set." >&2
            exit 1
        fi
        create_directory_if_not_exists_or_exit "$STATIC_FILES_DEFAULT"
        echo "Checking if files exist in $STATIC_FILES_DEFAULT..."
        if [ -z "$(ls -A $STATIC_FILES_DEFAULT)" ]; then
            echo "No files found in $STATIC_FILES_DEFAULT."
        else
            echo "Files found in $STATIC_FILES_DEFAULT. Removing them..."
            output=$(rm -rf "$STATIC_FILES_DEFAULT"/*)
            if [ $? -ne 0 ]; then
                echo "Failed to remove files from $STATIC_FILES_DEFAULT: $output" >&2
                exit 1
            fi
            echo "Files removed from $STATIC_FILES_DEFAULT."
        fi

    else
        if [ -z "$STATIC_FILES_DEFAULT" ]; then
            echo "ENV is not set to COLLECT_STATIC and STATIC_FILES_DEFAULT is not set. Static files are not needed."
        else 
            echo "ENV is not set to COLLECT_STATIC and STATIC_FILES_DEFAULT is set. Static files are needed. "\
                "Setting up the filesystem..."
            if [ -z "$(ls -A $STATIC_FILES_DEFAULT)" ]; then
                echo "No files found in $STATIC_FILES_DEFAULT. Abort." >&2
                exit 1
            else
                if [ "$STATIC_FILES_DEFAULT" = "$STATIC_FILES" ]; then
                    echo "STATIC_FILES_DEFAULT is not empty and STATIC_FILES is set to STATIC_FILES_DEFAULT. "\
                        "The static files are already set up."
                else
                    echo "STATIC_FILES_DEFAULT is not empty and STATIC_FILES is not set to STATIC_FILES_DEFAULT. "\
                        "Setting up the filesystem..."
                    create_directory_if_not_exists_or_exit "$STATIC_FILES"
                    echo "Checking if files exist in $STATIC_FILES..."
                    if [ -z "$(ls -A $STATIC_FILES)" ]; then
                        echo "No files found in $STATIC_FILES."
                    else
                        echo "Files found in $STATIC_FILES. Removing them..."
                        output=$(rm -rf "$STATIC_FILES"/*)
                        if [ $? -ne 0 ]; then
                            echo "Failed to remove files from $STATIC_FILES: $output" >&2
                            exit 1
                        fi
                        echo "Files removed from $STATIC_FILES."
                    fi
                    echo "$STATIC_FILES is empty. Copying files from $STATIC_FILES_DEFAULT to $STATIC_FILES..."
                    output=$(cp -r "$STATIC_FILES_DEFAULT"/* "$STATIC_FILES")
                    if [ $? -ne 0 ]; then
                        echo "Failed to copy files from $STATIC_FILES_DEFAULT to $STATIC_FILES: $output" >&2
                        exit 1
                    fi
                    echo "Files copied from $STATIC_FILES_DEFAULT to $STATIC_FILES."
                fi
            fi
        fi
    fi
    echo "Static files are set up."
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