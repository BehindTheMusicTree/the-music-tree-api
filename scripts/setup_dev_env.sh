#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/

bash "${SCRIPT_DIR}setup_filesystem.sh"
bash "${SCRIPT_DIR}run_db_and_afp_containers.sh"