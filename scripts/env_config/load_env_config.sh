#!/bin/bash

# Get the directory of the script even when it's called from another script
SCRIPT_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
echo "SCRIPT_DIR $SCRIPT_DIR"
ENV_PATH="$SCRIPT_DIR../../env/.env"

if [ -f "$ENV_PATH" ]; then
    echo "Loading environment variables from ${ENV_PATH}"
    while IFS='=' read -r key value
    do
        # Skip comments and empty lines
        if [ -z "$key" ]; then continue; fi
        export "$key=$value"
    done < "$ENV_PATH"

	if [ -z $ENV ]; then
		echo "ENV is not set in the .env file"
		exit 1
    fi
else
    echo "$ENV_PATH env file does not exist"
fi

CONFIG_PATH="$SCRIPT_DIR../../env/config/config.json"
if [ ! -f "$CONFIG_PATH" ]; then
    echo "Configuration file '${CONFIG_PATH}' was not found."
    exit 1
else
    echo "Loading configuration values from ${CONFIG_PATH}"
fi

config=$(cat "$CONFIG_PATH")
currentEnvLower=$(echo "$ENV" | tr '[:upper:]' '[:lower:]')

envConfig=$(echo "$config" | jq -r --arg env "$currentEnvLower" '.["environments"][$env]')

export EXTERNAL_DIRS_NEEDED=$(echo "$envConfig" | jq -r '.["externalDirsNeeded"]')

defaultInternalPaths=$(echo "$config" | jq -r '.["defaultInternalPaths"]')

export MEDIA_DEFAULT_INTERNAL_DIR=$(echo "$defaultInternalPaths" | jq -r '.["media"]')
export LIBRARIES_DEFAULT_INTERNAL_DIR_NAME=$(echo "$defaultInternalPaths" | jq -r '.["librariesDirName"]')
export STATIC_FILES_DEFAULT_INTERNAL_DIR=$(echo "$defaultInternalPaths" | jq -r '.["staticFiles"]')
export LOG_DEFAULT_INTERNAL_DIR=$(echo "$defaultInternalPaths" | jq -r '.["log"]')
export TMP_UPLOADED_FILES_DEFAULT_INTERNAL_DIR=$(echo "$defaultInternalPaths" | jq -r '.["tmpUploadedFiles"]')