#!/bin/bash

SCRIPTS_DIR=$(dirname "$0")/../

# Load environment variables in the current shell
source "${SCRIPTS_DIR}load_config.sh"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME;"

# Display all databases
DATABASES=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -t -c "SELECT datname FROM pg_database;")
echo "All databases: $DATABASES"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME \
psql -d $DB_BODZIFY_API_DB_NAME -c "CREATE USER $DB_BODZIFY_API_USERNAME WITH PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';"

# Display all users
USERS=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME \
psql -t -c "SELECT rolname FROM pg_roles WHERE rolcanlogin = true;")
echo "All users: $USERS"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c \
"psql -c \"GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;\"; \
psql -c \"ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';\"; \
psql -c \"ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';\"; \
psql -c \"ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';\"; \
psql -c \"ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;\"; \
psql -d $DB_BODZIFY_API_DB_NAME -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_BODZIFY_API_USERNAME;\"; \
psql -d $DB_BODZIFY_API_DB_NAME -c \"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $DB_BODZIFY_API_USERNAME;\""