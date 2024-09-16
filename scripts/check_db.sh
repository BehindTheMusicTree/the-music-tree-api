#!/bin/bash

# Source the utils.sh file to include the check_if_db_empty_or_exit function
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"/
source ${SCRIPTS_DIR}utils.sh

# Call the function
check_if_db_empty_or_exit