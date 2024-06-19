#!/bin/bash

echo "Loading environment variables..."
while IFS= read -r line
do
  if [[ ! $line == \#* ]]; then
    export $line
    echo "${line%%=*}"
  fi
done < "${PROJECT_PATH}.env"