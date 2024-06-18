#!/bin/bash

# creating the role automatically creates a database with the same name
docker exec -u postgres $DB_CONTAINER_NAME psql <<EOF
CREATE ROLE $DB_BODZIFY_API_USERNAME WITH LOGIN PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE $DB_BODZIFY_API_DB_NAME TO $DB_BODZIFY_API_USERNAME;
ALTER ROLE $DB_BODZIFY_API_USERNAME SET client_encoding TO 'utf8';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_BODZIFY_API_USERNAME SET timezone TO 'UTC';
ALTER USER $DB_BODZIFY_API_USERNAME CREATEDB;
EOF

echo "Testing database connection..."
export PGPASSWORD=$DB_BODZIFY_API_USER_PASSWORD
psql -h localhost -p $DB_PORT -U $DB_BODZIFY_API_USERNAME -d $DB_BODZIFY_API_DB_NAME -c "\q"
if [ $? -eq 0 ]
then
  echo "Database connection test passed."
else
  echo "Database connection test failed."
  exit 1
fi
unset PGPASSWORD

projectDir=./
managePath=$projectDir/manage.py
python3 $managePath migrate
python3 $managePath migrate --fake
python3 $managePath makemigrations 
python3 $managePath migrate
python3 $managePath makemigrations bodzify_api
python3 $managePath migrate
python3 $managePath loaddata app
python3 $managePath loaddata admin_user_dev
python3 $managePath loaddata mobile_test_user
python3 $managePath loaddata postman_test_user
python3 $managePath loaddata ultimate_music_guide_test_user_dev