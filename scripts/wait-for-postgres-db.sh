#!/bin/bash

# Usage: ./wait-for-postgres-db.sh <DB_HOST> <DB_PORT> [MAX_ATTEMPTS] [SLEEP_INTERVAL]
# Example: ./wait-for-postgres-db.sh localhost 5432 10 5

DB_HOST=$1
DB_PORT=$2
MAX_ATTEMPTS=${3:-10}
SLEEP_INTERVAL=${4:-5}

attempts=0

echo "Waiting for DB service to start..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT"; do
  if [ "$attempts" -eq "$MAX_ATTEMPTS" ]; then
    echo "DB service did not start within the expected time."
    exit 1
  fi
  echo "Waiting for DB service to start..."
  sleep "$SLEEP_INTERVAL"
  attempts=$((attempts+1))
done

echo "DB service is up and running."