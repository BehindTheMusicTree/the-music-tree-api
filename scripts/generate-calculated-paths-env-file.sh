#!/bin/bash

calculate_static_files_dir(){
    if [ $ENV = "COLLECT_STATIC" ]; then
        log "ENV is set to COLLECT_STATIC. Calculating the static files directory..."
        check_vars_are_set STATIC_FILES_INTERNAL
        if [ -n "$STATIC_FILES_EXTERNAL" ]; then
            log "ERROR: In collect static mode, $STATIC_FILES_EXTERNAL must not be set." >&2
            exit 1
        fi
    else 
        if [ -z "$STATIC_FILES_INTERNAL" ]; then
            log "ENV is not set to COLLECT_STATIC and STATIC_FILES_INTERNAL is not set. Static files are not needed."
            if [ -n "$STATIC_FILES_EXTERNAL" ]; then
                log "ERROR: STATIC_FILES_EXTERNAL must not be set if STATIC_FILES_INTERNAL is not set." >&2
                exit 1
            fi
        else
            if [ $STATIC_FILES_INTERNAL = $STATIC_FILES_EXTERNAL ]; then
                log "ERROR: STATIC_FILES_INTERNAL and STATIC_FILES_EXTERNAL must not be set to the same value." >&2
                exit 1
            fi
        fi
    fi
    
    if [ -n "$STATIC_FILES_INTERNAL" ]; then
        log "STATIC_FILES_INTERNAL is set. Setting the static files default directory to internal."
        STATIC_FILES_DEFAULT="${PROJECT_DIR}${STATIC_FILES_INTERNAL}"
        if [ -n "$STATIC_FILES_EXTERNAL" ]; then
            log "STATIC_FILES_EXTERNAL is set. Setting the static files directory to external."
            STATIC_FILES="${STATIC_FILES_EXTERNAL}"
        else
            log "STATIC_FILES_EXTERNAL is not set. Setting the static files directory to internal."
            STATIC_FILES="${STATIC_FILES_DEFAULT}"
        fi
        log "STATIC_FILES_DEFAULT is set to $STATIC_FILES_DEFAULT"
        log "STATIC_FILES is set to $STATIC_FILES"
        echo "STATIC_FILES_DEFAULT=$STATIC_FILES_DEFAULT" >> "$CALCULATED_PATHS_ENV_FILE"
        echo "STATIC_FILES=$STATIC_FILES" >> "$CALCULATED_PATHS_ENV_FILE"
    fi
}

calculate_django_log_dir(){
    if [ -n "$DJANGO_LOG_DIR_EXTERNAL" ]; then
        if [ -n "$DJANGO_LOG_DIR_INTERNAL" ]; then
            log "ERROR: DJANGO_LOG_DIR_INTERNAL and DJANGO_LOG_DIR_EXTERNAL must not be set at the same time." >&2
            exit 1
        fi
        log "DJANGO_LOG_DIR_EXTERNAL is set. Setting the Django logs to external."
        DJANGO_LOG_DIR="${DJANGO_LOG_DIR_EXTERNAL}"
    else
        if [ -n "$DJANGO_LOG_DIR_INTERNAL" ]; then
            log "DJANGO_LOG_DIR_INTERNAL is set. Setting the Django logs to internal."
            DJANGO_LOG_DIR="${PROJECT_DIR}${DJANGO_LOG_DIR_INTERNAL}"
        else
            log "Neither DJANGO_LOG_DIR_EXTERNAL nor DJANGO_LOG_DIR_INTERNAL is set. Django logs are not needed."
        fi
    fi

    if [ -n "$DJANGO_LOG_DIR" ]; then
        log "DJANGO_LOG_DIR is set to $DJANGO_LOG_DIR"
        echo "DJANGO_LOG_DIR=$DJANGO_LOG_DIR" >> "$CALCULATED_PATHS_ENV_FILE"
    fi
}

calculate_media_dirs(){
    if [ -n "$TMP_UPLOADED_FILES_EXTERNAL" ]; then
        if [ -n "$TMP_UPLOADED_FILES_INTERNAL" ]; then
            log "ERROR: TMP_UPLOADED_FILES_INTERNAL and TMP_UPLOADED_FILES_EXTERNAL must not be set at the same "\
                "time." >&2
            exit 1
        fi
        log "TMP_UPLOADED_FILES_EXTERNAL is set. Setting the temporary files directory to external."
        TMP_UPLOADED_FILES="${TMP_UPLOADED_FILES_EXTERNAL}"
    else
        if [ -n "$TMP_UPLOADED_FILES_INTERNAL" ]; then
            log "TMP_UPLOADED_FILES_INTERNAL is set. Setting the temporary files directory to internal."
            TMP_UPLOADED_FILES="${PROJECT_DIR}${TMP_UPLOADED_FILES_INTERNAL}"
        else
            log "Neither TMP_UPLOADED_FILES_EXTERNAL nor TMP_UPLOADED_FILES_INTERNAL is set." \
                "The app will not handle media files."
        fi
    fi

    if [ -n "$TMP_UPLOADED_FILES" ]; then
        log "TMP_UPLOADED_FILES is set to $TMP_UPLOADED_FILES"
        echo "TMP_UPLOADED_FILES=$TMP_UPLOADED_FILES" >> "$CALCULATED_PATHS_ENV_FILE"

        log "As TMP_UPLOADED_FILES is set, setting up media directories..."
        if [ -n "$MEDIA_DIR_EXTERNAL" ]; then
            if [ -n "$MEDIA_DIR_INTERNAL" ]; then
                log "ERROR: MEDIA_DIR_INTERNAL and MEDIA_DIR_EXTERNAL must not be set at the same time." >&2
                exit 1
            fi
            log "MEDIA_DIR_EXTERNAL is set. Setting media directory to external..."
            MEDIA_DIR="${MEDIA_DIR_EXTERNAL}"
        else
            if [ -n "$MEDIA_DIR_INTERNAL" ]; then
                log "MEDIA_DIR_INTERNAL is set. Setting media directory to internal..."
                MEDIA_DIR="${PROJECT_DIR}${MEDIA_DIR_INTERNAL}"
            else
                log "ERROR: Neither MEDIA_DIR_EXTERNAL nor MEDIA_DIR_INTERNAL is set. Abort." >&2
                exit 1
            fi
        fi
        log "MEDIA_DIR is set to $MEDIA_DIR"
        echo "MEDIA_DIR=$MEDIA_DIR" >> "$CALCULATED_PATHS_ENV_FILE"

        log "Setting up libraries directory..."
        check_vars_are_set "LIBRARIES_DIR_NAME"
        LIBRARIES_DIR="${MEDIA_DIR}${LIBRARIES_DIR_NAME}/"
        log "LIBRARIES_DIR is set to $LIBRARIES_DIR"
        echo "LIBRARIES_DIR=$LIBRARIES_DIR" >> "$CALCULATED_PATHS_ENV_FILE"
        log "Libraries directory is set up."
    else
        if [ -n "$MEDIA_DIR_EXTERNAL" ]; then
            log "ERROR: MEDIA_DIR_EXTERNAL must not be set if TMP_UPLOADED_FILES_INTERNAL is not set." >&2
            exit 1
        fi
        if [ -n "$LIBRARIES_DIR_NAME" ]; then
            log "ERROR: LIBRARIES_DIR_NAME must not be set if TMP_UPLOADED_FILES_INTERNAL is not set." >&2
            exit 1
        fi
    fi
}

main () {
    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
    CALCULATED_PATHS_ENV_FILE="${PROJECT_DIR}env/calculated_paths/.env"
    source ${SCRIPTS_DIR}utils.sh

    log "Generating the env file with calculated paths..."

    check_vars_are_set ENV

    [ -f "$CALCULATED_PATHS_ENV_FILE" ] && rm -f "$CALCULATED_PATHS_ENV_FILE"
    output=$(touch "$CALCULATED_PATHS_ENV_FILE")
    if [ $? -ne 0 ]; then
        log "ERROR: Failed to create the generated paths env file: $output" >&2
        exit 1
    fi

    calculate_media_dirs
    calculate_static_files_dir
    calculate_django_log_dir
    
    log "Generated the env file with calculated paths successfully."
}

main "$@"