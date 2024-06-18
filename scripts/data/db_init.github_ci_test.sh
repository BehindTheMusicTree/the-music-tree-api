#!/bin/bash

# Creating the role automatically creates a database with the same name
# docker exec -u postgres $DB_CONTAINER_NAME psql <<EOF
# CREATE ROLE $DB_BODZIFY_API_USERNAME WITH LOGIN PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';
# GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;
# ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';
# ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';
# ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';
# ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;
# EOF

DB_CREATION_OUTPUT=$(docker exec -u postgres DB psql -c 'CREATE DATABASE bod_table;' 2>&1)

# Display all databases
DATABASES=$(docker exec -u postgres DB psql -t -c "SELECT datname FROM pg_database;")
echo "All databases: $DATABASES"

docker exec -u postgres DB psql -d bod_table <<EOF
CREATE USER django WITH PASSWORD 'hehe';
EOF

# Display all users
USERS=$(docker exec -u postgres DB psql -t -c "SELECT rolname FROM pg_roles WHERE rolcanlogin = true;")
echo "All users: $USERS"

docker exec -u postgres DB bash -c "PGPASSWORD=$DB_SUPERUSER_PASSWORD psql -v ON_ERROR_STOP=1" <<EOF
GRANT ALL PRIVILEGES ON DATABASE bod_table TO django;
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
ALTER USER django CREATEDB;
EOF

# test if the role was created
# ROLE=$(docker exec -u postgres $DB_CONTAINER_NAME psql -c "SELECT rolname FROM pg_roles WHERE rolname='$DB_BODZIFY_API_DB_NAME';")
# if [ $? -eq 0 ]; then
#     echo "Role $DB_BODZIFY_API_USERNAME created successfully"
# else
#     echo "Role $DB_BODZIFY_API_USERNAME creation failed"
# fi

ROLE=$(docker exec -u postgres DB psql -t -c "SELECT rolname FROM pg_roles WHERE rolname='django';")
echo "Output of role check: $ROLE"

if [ "$ROLE" = "django" ]; then
    echo "Role django exists"
else
    echo "Role django does not exist"
fi