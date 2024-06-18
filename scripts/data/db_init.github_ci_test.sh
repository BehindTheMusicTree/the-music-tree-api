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
docker exec -u postgres $DB_CONTAINER_NAME psql <<EOF
CREATE ROLE django WITH LOGIN PASSWORD 'hehe';
GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;
ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';
ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;
EOF

# test if the role was created
docker exec -u postgres $DB_CONTAINER_NAME psql -c "SELECT * FROM pg_roles;" $DB_BODZIFY_API_DB_NAME
if [ $? -eq 0 ]; then
    echo "Role $DB_BODZIFY_API_USERNAME created successfully"
else
    echo "Role $DB_BODZIFY_API_USERNAME creation failed"
fi