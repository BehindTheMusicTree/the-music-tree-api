#!/bin/bash

# WARNING: This script will reinitialize the Django database.
# Use with caution as it may result in data loss.

echo "WARNING: This script will reinitialize the Django database."
echo "Use with caution as it may result in data loss."
read -p "Are you sure you want to proceed? (yes/no): " CONFIRMATION

if [ "$CONFIRMATION" != "yes" ]; then
    echo "Operation aborted."
    exit 1
fi

REQUIRED_NON_BOOL_VARS=(
    APP_NAME
    LIBRARIES_DIR
    DB_BODZIFY_API_DB_NAME
    DB_PORT
    DB_SUPERUSER_NAME
    DB_SUPERUSER_PASSWORD
    DB_BODZIFY_API_USERNAME
)
for VAR in "${REQUIRED_NON_BOOL_VARS[@]}"; do
    check_var_is_set "$VAR"
done
check_bool_var_is_set "APP_IS_EXPOSED"

# Get the directory of the script even when it's called from another script
SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/

echo "Running purge script..."
bash ${SCRIPTS_DIR}purge_django_data_USE_WITH_CAUTION.sh -s
if [ $? -ne 0 ]; then
  echo "Failed to purge Django data. Aborting." >&2
  exit 1
fi

echo "Running Django data init script..."
bash ${SCRIPTS_DIR}init_django_data.sh -s
if [ $? -ne 0 ]; then
  echo "Failed to initialize data. Aborting." >&2
  exit 1
fi

echo "Django data reinitialized successfully."