#!/bin/bash

# creating the role automatically creates a database with the same name
docker exec -u postgres $DB_CONTAINER_NAME \
psql -c "CREATE ROLE $DB_BODZIFY_API_USERNAME WITH LOGIN PASSWORD '$DB_BODZIFY_API_USER_PASSWORD';"

echo "List of databases:"
docker exec -u postgres $DB_CONTAINER_NAME psql -c "\l"

echo "List of roles:"
docker exec -u postgres $DB_CONTAINER_NAME psql -c "\du"

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