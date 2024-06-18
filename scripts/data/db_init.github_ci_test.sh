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
docker exec -u postgres DB psql <<EOF
CREATE ROLE django WITH LOGIN PASSWORD 'hehe';
GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;
ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';
ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;
EOF

# test if the role was created
# ROLE=$(docker exec -u postgres $DB_CONTAINER_NAME psql -c "SELECT rolname FROM pg_roles WHERE rolname='$DB_BODZIFY_API_DB_NAME';")
# if [ $? -eq 0 ]; then
#     echo "Role $DB_BODZIFY_API_USERNAME created successfully"
# else
#     echo "Role $DB_BODZIFY_API_USERNAME creation failed"
# fi

ROLE=$(docker exec -u postgres $DB_CONTAINER_NAME psql -t -c "SELECT rolname FROM pg_roles WHERE rolname='django';")
if [ "$ROLE" = "django" ]; then
    echo "Role django created successfully"
else
    echo "Role django creation failed"
fi