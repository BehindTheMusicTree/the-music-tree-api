#!/bin/bash

DB_CREATION_OUTPUT=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME \
psql -c "CREATE DATABASE $DB_BODZIFY_API_DB_NAME;" 2>&1)

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
"psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;\""

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c \
"psql -c "ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';\""

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c \
"psql -c "ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';\""

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c \
"psql -c "ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';\""

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c \
"psql -c "ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;\""