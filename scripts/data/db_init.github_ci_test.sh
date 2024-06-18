#!/bin/bash

DB_CREATION_OUTPUT=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -c 'CREATE DATABASE bod_table;' 2>&1)

# Display all databases
DATABASES=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -t -c "SELECT datname FROM pg_database;")
echo "All databases: $DATABASES"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -d bod_table -c "CREATE USER $DB_BODZIFY_API_USERNAME WITH PASSWORD 'hehe';"

# Display all users
USERS=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -t -c "SELECT rolname FROM pg_roles WHERE rolcanlogin = true;")
echo "All users: $USERS"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c "PGPASSWORD=$DB_SUPERUSER_PASSWORD psql -v ON_ERROR_STOP=1" <<EOF
GRANT ALL PRIVILEGES ON DATABASE bod_table TO $DB_BODZIFY_API_USERNAME;
ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';
ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;
EOF