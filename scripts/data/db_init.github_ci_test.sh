#!/bin/bash

DB_CREATION_OUTPUT=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -c 'CREATE DATABASE bod_table;' 2>&1)

# Display all databases
DATABASES=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -t -c "SELECT datname FROM pg_database;")
echo "All databases: $DATABASES"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -d bod_table -c "CREATE USER django WITH PASSWORD 'hehe';"

# Display all users
USERS=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -t -c "SELECT rolname FROM pg_roles WHERE rolcanlogin = true;")
echo "All users: $USERS"

docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME bash -c "PGPASSWORD=$DB_SUPERUSER_PASSWORD psql -v ON_ERROR_STOP=1" <<EOF
GRANT ALL PRIVILEGES ON DATABASE bod_table TO django;
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
ALTER USER django CREATEDB;
EOF

ROLE=$(docker exec -u $DB_SUPERUSER_NAME $DB_CONTAINER_NAME psql -t -c "SELECT rolname FROM pg_roles WHERE rolname='django';")
echo "Output of role check: $ROLE"

if [ "$ROLE" = "django" ]; then
    echo "Role django exists"
else
    echo "Role django does not exist"
fi