#!/bin/bash

check_vars_are_set() {
    local missing_vars=()
    for var_name in "$@"; do
        if [ -z "${!var_name}" ]; then
            echo "$var_name is not set" >&2
            exit 1
        fi
    done
}

check_bool_vars_are_set() {
    local invalid_vars=()
    for var_name in "$@"; do
        if [ -z "${!var_name}" ]; then
            echo "$var_name is not set" >&2
            invalid_vars+=("$var_name")
        elif [ "${!var_name}" != "true" ] && [ "${!var_name}" != "false" ]; then
            echo "$var_name is not a valid boolean (true/false)" >&2
            invalid_vars+=("$var_name")
        fi
    done

    if [ ${#invalid_vars[@]} -ne 0 ]; then
        echo "The following boolean variables are invalid: ${invalid_vars[*]}" >&2
        exit 1
    fi
}

export_value_removing_surrounding_quotes() {
    local VAR_NAME=$1
    local VAR_VALUE=${!VAR_NAME}
    VAR_VALUE=${VAR_VALUE#\'}
    VAR_VALUE=${VAR_VALUE%\'}
    export "$VAR_NAME=$VAR_VALUE"
}

load_project_env_file_if_exists() {
    local SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    local PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
    local ENV_FILE=${PROJECT_DIR}env/.env
    if [ ! -f "$ENV_FILE" ]; then
        echo "$ENV_FILE env file does not exist."
    else
        echo "Loading environment variables from ${ENV_FILE} ..."
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            if [ -z "$key" ]; then continue; fi
            export "$key=$value"
        done < "$ENV_FILE"
    fi
}

load_project_calculated_paths_env_vars() {
    echo "Loading calculated paths..."

    check_vars_are_set "LIBRARIES_DIR_NAME"
    REQUIRED_BOOL_VARS=(
        "APP_IS_EXPOSED"
        "STATIC_FILES_ARE_NEEDED"
        "DJANGO_LOGS_ARE_NEEDED"
        "AUDIO_META_ANALYSE_IS_NEEDED"
    )
    check_bool_vars_are_set ${REQUIRED_BOOL_VARS[@]}

    local SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    local PROJECT_DIR=$(realpath "${SCRIPTS_DIR}..")/
    local CALTULATED_PATHS_DIR="${PROJECT_DIR}env/calculated_paths/"

    if [ ! -d "$CALTULATED_PATHS_DIR" ]; then
        echo "$CALTULATED_PATHS_DIR directory does not exist" >&2
        exit 1
    fi

    local CALCULATED_PATHS_ENV_FILE="${CALTULATED_PATHS_DIR}.env"
    bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh"
    
    echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$CALCULATED_PATHS_ENV_FILE"
    echo "Calculated paths loaded successfully."
}