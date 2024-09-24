#!/bin/bash

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
source "${SCRIPTS_DIR}utils.sh"

log_with_script_prefixe () {
    log "[Django data initialized checker] $1"
}

output=$(python manage.py check_data_initialized > /dev/null 2>&1)
if [ $? -ne 0 ]; then
    log_with_script_prefixe "Django data is not initialized." >&2
    exit 1
fi
log_with_script_prefixe "Django data is initialized."