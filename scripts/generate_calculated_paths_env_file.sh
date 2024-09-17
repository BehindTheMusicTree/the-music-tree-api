#!/bin/bash

calculate_static_files_dir(){
    if [ -n "$STATIC_FILES_INTERNAL" ]; then
        echo "STATIC_FILES_INTERNAL is set. Static files are needed."
        STATIC_FILES_DEFAULT="${APP_DIR}${STATIC_FILES_INTERNAL}"
        if [ -n "$STATIC_FILES_EXTERNAL" ]; then
            echo "STATIC_FILES_EXTERNAL is set. Setting static files to external."
            STATIC_FILES="${STATIC_FILES_EXTERNAL}"
        else
            echo "STATIC_FILES_EXTERNAL is not set. Setting static files to internal."
            STATIC_FILES="${STATIC_FILES_DEFAULT}"
        fi

        echo "STATIC_FILES is set to $STATIC_FILES"
        echo "STATIC_FILES_DEFAULT=$STATIC_FILES_DEFAULT" >> "$CALCULATED_PATHS_ENV_FILE"
        echo "STATIC_FILES=$STATIC_FILES" >> "$CALCULATED_PATHS_ENV_FILE"
    else
        if [ -n "$STATIC_FILES_EXTERNAL" ]; then
            echo "STATIC_FILES_EXTERNAL must not be set if STATIC_FILES_INTERNAL is not set." >&2
            exit 1
        fi
    fi
}

calculate_django_log_dir(){
    if [ -n "$DJANGO_LOG_DIR_EXTERNAL" ]; then
        if [ -n "$DJANGO_LOG_DIR_INTERNAL" ]; then
            echo "DJANGO_LOG_DIR_INTERNAL and DJANGO_LOG_DIR_EXTERNAL must not be set at the same time." >&2
            exit 1
        fi
        echo "DJANGO_LOG_DIR_EXTERNAL is set. Setting the Django logs to external."
        DJANGO_LOG_DIR="${DJANGO_LOG_DIR_EXTERNAL}"
    else
        if [ -n "$DJANGO_LOG_DIR_INTERNAL" ]; then
            echo "DJANGO_LOG_DIR_INTERNAL is set. Setting the Django logs to internal."
            DJANGO_LOG_DIR="${APP_DIR}${DJANGO_LOG_DIR_INTERNAL}"
        else
            echo "Neither DJANGO_LOG_DIR_EXTERNAL nor DJANGO_LOG_DIR_INTERNAL is set. Django logs are not needed."
        fi
    fi

    if [ -n "$DJANGO_LOG_DIR" ]; then
        echo "DJANGO_LOG_DIR is set to $DJANGO_LOG_DIR"
        echo "DJANGO_LOG_DIR=$DJANGO_LOG_DIR" >> "$CALCULATED_PATHS_ENV_FILE"
    fi
}

calculate_media_dirs(){
    if [ -n "$TMP_UPLOADED_FILES_EXTERNAL" ]; then
        if [ -n "$TMP_UPLOADED_FILES_INTERNAL" ]; then
            echo "TMP_UPLOADED_FILES_INTERNAL and TMP_UPLOADED_FILES_EXTERNAL must not be set at the same time." >&2
            exit 1
        fi
        echo "TMP_UPLOADED_FILES_EXTERNAL is set. Setting the temporary files directory to external."
        TMP_UPLOADED_FILES="${TMP_UPLOADED_FILES_EXTERNAL}"
    else
        if [ -n "$TMP_UPLOADED_FILES_INTERNAL" ]; then
            echo "TMP_UPLOADED_FILES_INTERNAL is set. Setting the temporary files directory to internal."
            TMP_UPLOADED_FILES="${APP_DIR}${TMP_UPLOADED_FILES_INTERNAL}"
        else
            echo "Neither TMP_UPLOADED_FILES_EXTERNAL nor TMP_UPLOADED_FILES_INTERNAL is set." \
                "The app will not handle media files."
        fi
    fi

    if [ -n "$TMP_UPLOADED_FILES" ]; then
        echo "TMP_UPLOADED_FILES is set to $TMP_UPLOADED_FILES"
        echo "TMP_UPLOADED_FILES=$TMP_UPLOADED_FILES" >> "$CALCULATED_PATHS_ENV_FILE"

        echo "As TMP_UPLOADED_FILES is set, setting up media directories..."
        if [ -n "$MEDIA_DIR_EXTERNAL" ]; then
            if [ -n "$MEDIA_DIR_INTERNAL" ]; then
                echo "MEDIA_DIR_INTERNAL and MEDIA_DIR_EXTERNAL must not be set at the same time." >&2
                exit 1
            fi
            echo "MEDIA_DIR_EXTERNAL is set. Setting media directory to external..."
            MEDIA_DIR="${MEDIA_DIR_EXTERNAL}"
        else
            if [ -n "$MEDIA_DIR_INTERNAL" ]; then
                echo "MEDIA_DIR_INTERNAL is set. Setting media directory to internal..."
                MEDIA_DIR="${APP_DIR}${MEDIA_DIR_INTERNAL}"
            else
                echo "Neither MEDIA_DIR_EXTERNAL nor MEDIA_DIR_INTERNAL is set. Abort." >&2
                exit 1
            fi
        fi
        echo "MEDIA_DIR is set to $MEDIA_DIR"
        echo "MEDIA_DIR=$MEDIA_DIR" >> "$CALCULATED_PATHS_ENV_FILE"

        echo "Setting up libraries directory..."
        check_vars_are_set "LIBRARIES_DIR_NAME"
        LIBRARIES_DIR="${MEDIA_DIR}${LIBRARIES_DIR_NAME}/"
        echo "LIBRARIES_DIR is set to $LIBRARIES_DIR"
        echo "LIBRARIES_DIR=$LIBRARIES_DIR" >> "$CALCULATED_PATHS_ENV_FILE"
        echo "Libraries directory is set up."
    else
        if [ -n "$MEDIA_DIR_EXTERNAL" ]; then
            echo "MEDIA_DIR_EXTERNAL must not be set if TMP_UPLOADED_FILES_INTERNAL is not set." >&2
            exit 1
        fi
        if [ -n "$LIBRARIES_DIR_NAME" ]; then
            echo "LIBRARIES_DIR_NAME must not be set if TMP_UPLOADED_FILES_INTERNAL is not set." >&2
            exit 1
        fi
    fi
}

main () {
    echo "Generating the env file with calculated paths..."

    SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
    CALCULATED_PATHS_ENV_FILE="${APP_DIR}env/calculated_paths/.env"

    source ${SCRIPTS_DIR}utils.sh

    [ -f "$CALCULATED_PATHS_ENV_FILE" ] && rm -f "$CALCULATED_PATHS_ENV_FILE"
    output=$(touch "$CALCULATED_PATHS_ENV_FILE")
    if [ $? -ne 0 ]; then
        echo "Failed to create the generated paths env file: $output" >&2
        exit 1
    fi

    calculate_media_dirs
    calculate_static_files_dir
    calculate_django_log_dir
    
    echo "Generated the env file with calculated paths successfully."
}

main "$@"