#!/bin/bash

create_directory_if_not_exists_or_exit() {
    local dir_path=$1
    if [ ! -d "$dir_path" ]; then
        echo "Creating directory $dir_path ..."
        output=$(mkdir -p "$dir_path")
        if [ $? -ne 0 ]; then
            echo "Failed to create directory $dir_path : $output" >&2
            exit 1
        fi
        echo "Directory $dir_path created successfully."
        
    else
        echo "Directory $dir_path already exists"
    fi
}

touch_file_or_exit() {
    local file_path=$1
    echo "Touching file $file_path ..."
    output=$(touch "$file_path")
    if [ $? -ne 0 ]; then
        echo "Failed to create file $file_path : $output" >&2
        exit 1
    fi
    echo "File $file_path created successfully."
}

set_read_write_permissions_and_owner_or_exit() {
    local path=$1
    local user=$(whoami)
    output=$(chmod -R 740 "$path")
    if [ $? -ne 0 ]; then
        echo "Failed to change permissions of $path : $output" >&2
        exit 1
    fi
    output=$(chown -R "$user" "$path")
    if [ $? -ne 0 ]; then
        echo "Failed to change owner of $path : $output" >&2
        exit 1
    fi
}

check_vars_are_set() {
    local missing_vars=()
    for var_name in "$@"; do
        if [ -z "${!var_name}" ]; then
            echo "$var_name must be set." >&2
            exit 1
        fi
    done
}

check_bool_vars_are_set() {
    local invalid_vars=()
    check_vars_are_set "$@"
    for var_name in "$@"; do
        if [ "${!var_name}" != "true" ] && [ "${!var_name}" != "false" ]; then
            echo "$var_name is not a valid boolean (true/false)" >&2
            invalid_vars+=("$var_name")
        fi
    done

    if [ ${#invalid_vars[@]} -ne 0 ]; then
        echo "The following boolean variables are invalid: ${invalid_vars[*]}" >&2
        exit 1
    fi
}

export_value_removing_eventual_surrounding_quotes() {
    local VAR_NAME=$1
    local VAR_VALUE=${!VAR_NAME}
    VAR_VALUE=${VAR_VALUE#\'}
    VAR_VALUE=${VAR_VALUE%\'}
    export "$VAR_NAME=$VAR_VALUE"
}

load_app_env_file_if_exists() {
    local SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    local APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
    local ENV_FILE=${APP_DIR}env/.env
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
    check_bool_vars_are_set APP_IS_EXPOSED

    local SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
    local APP_DIR=$(realpath "${SCRIPTS_DIR}..")/
    local CALTULATED_PATHS_DIR="${APP_DIR}env/calculated_paths/"

    if [ ! -d "$CALTULATED_PATHS_DIR" ]; then
        echo "$CALTULATED_PATHS_DIR directory does not exist" >&2
        exit 1
    fi

    local CALCULATED_PATHS_ENV_FILE="${CALTULATED_PATHS_DIR}.env"
    bash "${SCRIPTS_DIR}generate_calculated_paths_env_file.sh"
    if [ $? -ne 0 ]; then
        echo "Failed to generate calculated paths env file: $output" >&2
        exit 1
    fi
    
    echo "Loading calculated paths from ${CALCULATED_PATHS_ENV_FILE}"
    while IFS='=' read -r key value; do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$CALCULATED_PATHS_ENV_FILE"
    echo "Calculated paths loaded successfully."
}

determine_db_host_if_not_set () {
    if [ -z "$DB_HOST" ]; then
        echo "DB_HOST is not set. Determining the host..."
        check_bool_vars_are_set APP_IS_EXPOSED
        if [ "$APP_IS_EXPOSED" = "true" ]; then
            check_vars_are_set DB_CONTAINER_NAME
            DB_HOST=$DB_CONTAINER_NAME
        else
            check_vars_are_set "DB_URL"
            DB_HOST=$DB_URL
        fi
        echo "DB_HOST: $DB_HOST"
        export DB_HOST
    fi
}