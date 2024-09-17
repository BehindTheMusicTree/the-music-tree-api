#!/bin/bash

# Usage: ./wait-for-postgres-db.sh <DB_HOST> <DB_PORT> [MAX_ATTEMPTS] [SLEEP_INTERVAL]
# Example: ./wait-for-postgres-db.sh localhost 5432 10 5

DB_HOST=$1
DB_PORT=$2
MAX_ATTEMPTS=${3:-10}
SLEEP_INTERVAL=${4:-5}

attempts=0

SCRIPTS_DIR=$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" || echo "${BASH_SOURCE[0]}")")" && pwd)/
APP_DIR=$(realpath "$(dirname "$SCRIPTS_DIR")")/
source "${SCRIPTS_DIR}utils.sh"

log "Waiting for DB service to start..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
  if [ "$attempts" -eq "$MAX_ATTEMPTS" ]; then
    log "ERROR: DB service did not start within the expected time." >&2
    exit 1
  fi
  log "Waiting for DB service to start..."
  sleep "$SLEEP_INTERVAL"
  attempts=$((attempts+1))
done

log "DB service is up and running."