#!/bin/bash

ENV_PATH="${PROJECT_PATH}.env"

if [ -f "$ENV_PATH" ]; then
    echo "Loading environment variables..."
    while IFS= read -r line
    do
      if [[ ! $line == \#* ]]; then
        export $line
        echo "${line%%=*}"
      fi
    done < "$ENV_PATH"
else
    echo "$ENV_PATH does not exist"
    exit 1
fi