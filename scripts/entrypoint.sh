#!/bin/bash

set -e

if [ -z "INIT_DB_AND_ROLE_SCRIPT" ]; then
    echo "INIT_DB_AND_ROLE_SCRIPT must be set." >&2
    exit 1
fi

bash ${INIT_DB_AND_ROLE_SCRIPT}

# Start the application
exec "$@"