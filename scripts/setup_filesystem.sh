#!/bin/bash

if [ -z "$1" ]; then
    echo "Error: no env file specified"
    exit 1
fi
APP_ENV_FILE="$1"

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
PROJECT_DIR=$(realpath $(dirname "$SCRIPTS_DIR"))/

echo "Loading environment variables from ${APP_ENV_FILE}"
while IFS='=' read -r key value
do
    # Skip comments and empty lines
    if [ -z "$key" ]; then continue; fi
    export "$key=$value"
done < "$APP_ENV_FILE"

check_bool_var() {
  local var_name="$1"
  local var_value="${!1}"
  if [ -z "$var_value" ]; then
    echo "$var_name is not set." >&2
    exit 1
  elif [ "$var_value" != "true" ] && [ "$var_value" != "false" ]; then
    echo "$var_name must be 'true' or 'false'." >&2
    exit 1
  fi
}

check_bool_var "APP_IS_EXPOSED"
check_bool_var "DJANGO_LOGS_ARE_NEEDED"
check_bool_var "STATIC_FILES_ARE_NEEDED"
check_bool_var "AUDIO_META_ANALYSE_IS_NEEDED"

if [ -z $LIBRARIES_DIR_NAME ]; then
  echo "LIBRARIES_DIR_NAME is not set" >&2
  exit 1
fi

CALCULATED_PATHS_ENV_FILE=$(cd "${PROJECT_DIR}env/calculated_paths/" && pwd)/.env
bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh" "$APP_ENV_FILE" "$PROJECT_DIR" "$CALCULATED_PATHS_ENV_FILE"

if [ $? -ne 0 ]; then
    echo "Failed to generate calculated paths env file"
    exit 1
fi

echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
while IFS='=' read -r key value
do
    export "$key=$value"
done < "$CALCULATED_PATHS_ENV_FILE"

if [ ! -d "$LIBRARIES_DIR" ]; then
    echo "Creating libraries directory"
    mkdir -p $LIBRARIES_DIR
else
    echo "Libraries directory $LIBRARIES_DIR already exists"
fi

if [ $STATIC_FILES_ARE_NEEDED = "true" ]; then
    if [ ! -d "$STATIC_FILES_DIR" ]; then
        echo "Creating static files directory $STATIC_FILES_DIR"
        mkdir -p $STATIC_FILES_DIR
    else
        echo "Static files directory $STATIC_FILES_DIR already exists"
    fi

    if [ -z $STATIC_FILES_DEFAULT_INTERNAL_DIR ]; then
        echo "STATIC_FILES_DEFAULT_INTERNAL_DIR is not set" >&2
        exit 1
    fi

    DEFAULT_STATIC_FILES_DIR="${PROJECT_DIR}$STATIC_FILES_DEFAULT_INTERNAL_DIR"
    if [ "$STATIC_FILES_DIR" != "$DEFAULT_STATIC_FILES_DIR" ]; then
        echo "STATIC_FILES_DIR is not the default internal directory. Moving static files to $STATIC_FILES_DIR"
        if [ ! -d $DEFAULT_STATIC_FILES_DIR ] or [ find "$DEFAULT_STATIC_FILES_DIR" -mindepth 1 -print -quit | grep -q ]; then
            echo "No static files found in default internal directory $STATIC_FILES_DEFAULT_INTERNAL_DIR"
        else
            mv $DEFAULT_STATIC_FILES_DIR/* $STATIC_FILES_DIR
            echo "Deleting default internal static files directory"
            rm -r $DEFAULT_STATIC_FILES_DIR
        fi
    else
        echo "STATIC_FILES_DIR is the default internal directory $DEFAULT_STATIC_FILES_DIR"
    fi
fi

if [ $DJANGO_LOGS_ARE_NEEDED = "true" ]; then
    if [ ! -d "$DJANGO_LOG_DIR" ]; then
        echo "Creating log directory $DJANGO_LOG_DIR"
        mkdir -p $DJANGO_LOG_DIR
    else
        echo "Log directory $DJANGO_LOG_DIR already exists"
    fi

    if [ -z $DJANGO_LOG_GENERAL_FILENAME ]; then
        echo "DJANGO_LOG_GENERAL_FILENAME is not set" >&2
        exit 1
    fi

    if [ -z $DJANGO_LOG_INFO_FILENAME ]; then
        echo "DJANGO_LOG_INFO_FILENAME is not set" >&2
        exit 1
    fi

    if [ -z $DJANGO_LOG_REQUESTS_FILENAME ]; then
        echo "DJANGO_LOG_REQUESTS_FILENAME is not set" >&2
        exit 1
    fi

    if [ -z $DJANGO_LOG_REQUESTS_DEBUG_FILENAME ]; then
        echo "DJANGO_LOG_REQUESTS_DEBUG_FILENAME is not set" >&2
        exit 1
    fi

    if [ -z $DJANGO_LOG_EXCEPTIONS_FILENAME ]; then
        echo "DJANGO_LOG_EXCEPTIONS_FILENAME is not set" >&2
        exit 1
    fi

    if [ -z $DJANGO_LOG_DJANGO_FILENAME ]; then
        echo "DJANGO_LOG_DJANGO_FILENAME is not set" >&2
        exit 1
    fi

    if [ -z $DJANGO_LOG_APP_FILENAME ]; then
        echo "DJANGO_LOG_APP_FILENAME is not set" >&2
        exit 1
    fi

    touch ${DJANGO_LOG_DIR}$DJANGO_LOG_GENERAL_FILENAME
    touch ${DJANGO_LOG_DIR}$DJANGO_LOG_INFO_FILENAME
    touch ${DJANGO_LOG_DIR}$DJANGO_LOG_REQUESTS_FILENAME
    touch ${DJANGO_LOG_DIR}$DJANGO_LOG_REQUESTS_DEBUG_FILENAME
    touch ${DJANGO_LOG_DIR}$DJANGO_LOG_EXCEPTIONS_FILENAME
    touch ${DJANGO_LOG_DIR}$DJANGO_LOG_DJANGO_FILENAME
    touch ${DJANGO_LOG_DIR}$DJANGO_LOG_APP_FILENAME
fi

if [ $APP_IS_EXPOSED = "true" ]; then
    if [ -z $GUNICORN_LOG_DIR ]; then
        echo "GUNICORN_LOG_DIR is not set while app is exposed" >&2
        exit 1
    fi

    if [ -z $GUNICORN_LOG_ERROR_FILENAME ]; then
        echo "GUNICORN_LOG_ERROR_FILENAME is not set while app is exposed" >&2
        exit 1
    fi

    if [ -z $GUNICORN_LOG_ACCESS_FILENAME ]; then
        echo "GUNICORN_LOG_ACCESS_FILENAME is not set while app is exposed" >&2
        exit 1
    fi

    if [ ! -d "$GUNICORN_LOG_DIR" ]; then
        echo "Creating Gunicorn log directory $GUNICORN_LOG_DIR"
        mkdir -p $GUNICORN_LOG_DIR
    else
        echo "Gunicorn log directory $GUNICORN_LOG_DIR already exists"
    fi

    touch ${GUNICORN_LOG_DIR}$GUNICORN_LOG_ERROR_FILENAME
    touch ${GUNICORN_LOG_DIR}$GUNICORN_LOG_ACCESS_FILENAME
else:
    echo "APP_IS_EXPOSED is set to false. Gunicorn logs are not needed."
fi

if [ $AUDIO_META_ANALYSE_IS_NEEDED = "true" ]; then
    if [ ! -d "$TMP_UPLOADED_FILES_DIR" ]; then
        echo "Creating temp uploaded files directory $TMP_UPLOADED_FILES_DIR"
        mkdir -p $TMP_UPLOADED_FILES_DIR
    else
        echo "Temp uploaded files directory $TMP_UPLOADED_FILES_DIR already exists"
    fi
else
    echo "AUDIO_META_ANALYSE_IS_NEEDED is set to false. Temp uploaded files dir is not needed."
fi

chmod 775 $MEDIA_DIR $STATIC_FILES_DIR $DJANGO_LOG_DIR $TMP_UPLOADED_FILES_DIR $GUNICORN_LOG_DIR