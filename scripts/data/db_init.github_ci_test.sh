#!/bin/bash

# creating the role automatically creates a database with the same name
# docker exec -u postgres $DB_CONTAINER_NAME psql <<EOF
# CREATE ROLE $DB_BODZIFY_API_USERNAME WITH LOGIN PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';
# GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;
# ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';
# ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';
# ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';
# ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;
# EOF

docker exec -u postgres DB bash -c "PGPASSWORD=$DB_SUPERUSER_PASSWORD psql" <<EOF
CREATE DATABASE bod_table;
EOF

if [ $? -ne 0 ]; then
  echo "Database creation failed."
else
  echo "Database created successfully."
fi

docker exec -u postgres DB bash -c "PGPASSWORD=$DB_SUPERUSER_PASSWORD psql -d bod_table" <<EOF
CREATE ROLE django WITH LOGIN PASSWORD 'hehe';
EOF

if [ $? -ne 0 ]; then
  echo "Role django creation failed."
else
  echo "Role django created successfully."
fi

ROLES=$(docker exec -u postgres DB psql -t -d bod_table -c "SELECT rolname FROM pg_roles;")
echo "All roles: $ROLES"

docker exec -u postgres DB bash -c "PGPASSWORD=$DB_SUPERUSER_PASSWORD psql -v ON_ERROR_STOP=1" <<EOF
GRANT ALL PRIVILEGES ON DATABASE bod_table TO django;
ALTER ROLE django SET client_encoding TO 'utf8';
ALTER ROLE django SET default_transaction_isolation TO 'read committed';
ALTER ROLE django SET timezone TO 'UTC';
ALTER USER django CREATEDB;
EOF

if [ $? -ne 0 ]; then
  echo "An error occurred while initializing the database."
else
  echo "Database initialized successfully."
fi

# Wait for a few seconds to ensure that the role creation is complete
sleep 5

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