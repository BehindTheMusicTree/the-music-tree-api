projectDir=~/Git/bodzify-api
managePath=~/Git/bodzify-api/manage.py
echo $managePath
sudo -u postgres dropdb -e bodzify_api -f
sudo -u postgres -H -- psql -c "create database bodzify_api with owner django;"
sudo rm -r $projectDir/bodzify_api/migrations/*
sudo rm -r /var/lib/bodzify-api/*
python3 $managePath migrate
python3 $managePath migrate --fake
python3 $managePath makemigrations 
python3 $managePath migrate
python3 $managePath makemigrations bodzify_api
python3 $managePath migrate
python3 $managePath loaddata initial_data
python3 $managePath loaddata initial_data_admin
python3 $managePath loaddata initial_data_test_app
python3 $managePath loaddata initial_data_test_postman
python3 $managePath runserver