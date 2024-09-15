#!/bin/bash

check_var_is_set() {
    local var_name=$1
    if [ -z "${!var_name}" ]; then
        echo "$var_name is not set" >&2
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