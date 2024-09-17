#!/bin/bash

load_env_vars () {
    log "Loading environment variables for the filesystem setup..."
    load_app_env_file_if_exists
    check_vars_are_set ENV
    check_bool_vars_are_set APP_IS_EXPOSED
    load_project_calculated_paths_env_vars
    log "Environment variables loaded for the filesystem setup."
}

setup_static_files_for_collection() {
    check_vars_are_set STATIC_FILES_DEFAULT 
    log "ENV is set to COLLECT_STATIC. Setting up the filesystem..."
    create_directory_if_not_exists_or_exit "$STATIC_FILES_DEFAULT"
    log "Checking if files exist in $STATIC_FILES_DEFAULT..."
    if [ -z "$(ls -A $STATIC_FILES_DEFAULT)" ]; then
        log "No files found in $STATIC_FILES_DEFAULT."
    else
        log "Files found in $STATIC_FILES_DEFAULT. Removing them..."
        output=$(rm -rf "$STATIC_FILES_DEFAULT"/*)
        if [ $? -ne 0 ]; then
            log "ERROR: Failed to remove files from $STATIC_FILES_DEFAULT: $output" >&2
            exit 1
        fi
        log "Files removed from $STATIC_FILES_DEFAULT."
    fi
}

setup_static_files_for_serving() {
    if [ -z "$STATIC_FILES_DEFAULT" ]; then
        log "ENV is not set to COLLECT_STATIC and STATIC_FILES_DEFAULT is not set. Static files are not needed."
    else 
        log "ENV is not set to COLLECT_STATIC and STATIC_FILES_DEFAULT is set. Static files are needed. "\
            "Setting up the filesystem..."
        log "Checking if the directory $STATIC_FILES_DEFAULT exists..."
        if [ ! -d "$STATIC_FILES_DEFAULT" ]; then
            log "ERROR: $STATIC_FILES_DEFAULT does not exist. Abort." >&2
            exit 1
        fi
        if [ -z "$(ls -A $STATIC_FILES_DEFAULT)" ]; then
            log "ERROR: No files found in $STATIC_FILES_DEFAULT. Abort." >&2
            exit 1
        else
            if [ "$STATIC_FILES_DEFAULT" = "$STATIC_FILES" ]; then
                log "STATIC_FILES_DEFAULT is not empty and STATIC_FILES is set to STATIC_FILES_DEFAULT. "\
                    "The static files are already set up."
            else
                log "STATIC_FILES_DEFAULT is not empty and STATIC_FILES is not set to STATIC_FILES_DEFAULT. "\
                    "Setting up the filesystem..."
                create_directory_if_not_exists_or_exit "$STATIC_FILES"
                log "Checking if files exist in $STATIC_FILES..."
                if [ -z "$(ls -A $STATIC_FILES)" ]; then
                    log "No files found in $STATIC_FILES ."
                else
                    log "Files found in $STATIC_FILES. Removing them..."
                    output=$(rm -rf "$STATIC_FILES"/*)
                    if [ $? -ne 0 ]; then
                        log "ERROR: Failed to remove files from $STATIC_FILES: $output" >&2
                        exit 1
                    fi
                    log "Files removed from $STATIC_FILES."
                fi
                log "$STATIC_FILES is empty. Moving files from $STATIC_FILES_DEFAULT to $STATIC_FILES..."
                output=$(mv "$STATIC_FILES_DEFAULT"/* "$STATIC_FILES")
                if [ $? -ne 0 ]; then
                    log "ERROR: Failed to move files from $STATIC_FILES_DEFAULT to $STATIC_FILES: $output" >&2
                    exit 1
                fi
                log "Files moved from $STATIC_FILES_DEFAULT to $STATIC_FILES."
                set_read_write_permissions_and_owner_or_exit "$STATIC_FILES"

                log "Removing the static files default directory..."
                output=$(rmdir "$STATIC_FILES_DEFAULT")
                if [ $? -ne 0 ]; then
                    log "ERROR: Failed to remove the static files default directory: $output" >&2
                    exit 1
                fi
                log "Static files default directory removed."
            fi
        fi
    fi
}
setup_django_log () {
    if [ -n "$DJANGO_LOGS_DIR" ]; then
        log "DJANGO_LOGS_DIR is set. Setting Django logs dirextories and files."
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
        log "DJANGO_LOGS_DIR is not set. Django logs are not needed."
    fi
}

setup_gunicorn_log () {
    if [ "$APP_IS_EXPOSED" = "true" ]; then
        log "App is exposed. Setting up Gunicorn logs."
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
        log "Gunicorn logs are set up."
    else
        log "APP_IS_EXPOSED is set to false. Gunicorn logs are not needed."
    fi
}

setup_media_dirs () {
    if [ -n "${TMP_UPLOADED_FILES}" ]; then
        log "TMP_UPLOADED_FILES is set. Setting up temp uploaded files directory and media direcroties..."
        create_directory_if_not_exists_or_exit "$TMP_UPLOADED_FILES"
        set_read_write_permissions_and_owner_or_exit "$TMP_UPLOADED_FILES"
        log "Temp uploaded files directory is set up."

        log "Setting up media directory..."
        create_directory_if_not_exists_or_exit "$MEDIA_DIR"
        create_directory_if_not_exists_or_exit "$LIBRARIES_DIR"
        set_read_write_permissions_and_owner_or_exit "$MEDIA_DIR"
        log "Media directories are set up."
    else
        log "TMP_UPLOADED_FILES is not set. The app will not handle media files."
    fi
}

main (){
    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    APP_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
    source "${SCRIPTS_DIR}utils.sh"
    
    log "Setting up filesystem..."

    load_env_vars
    check_vars_are_set ENV

    if [ $ENV = "COLLECT_STATIC" ]; then
        setup_static_files_for_collection
    else
        setup_static_files_for_serving
    fi

    log "Static files are set up."
    setup_django_log
    setup_gunicorn_log
    setup_media_dirs

    log "Making all scripts in $SCRIPTS_DIR executable..."
    for script in "${SCRIPTS_DIR}"*; do
        if [ -f "$script" ]; then
            output=$(chmod +x "$script")
            if [ $? -ne 0 ]; then
                log "ERROR: Failed to make $script executable: $output" >&2
                exit 1
            fi
        fi
    done
    log "All scripts in $SCRIPTS_DIR are now executable."

    log "The filesystem is set up."
}

main "$@"
