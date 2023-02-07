sudo -u postgres dropdb -e bodzify_api -f
sudo -u postgres -H -- psql -c "create database bodzify_api with owner django;"
sudo rm -r /var/lib/bodzify-api/*
sudo rm -r /var/log/bodzify-api/*

homeDir="/home/app/webapp"
python3 $homeDir/manage.py migrate
python3 $homeDir/manage.py migrate --fake
python3 $homeDir/manage.py makemigrations 
python3 $homeDir/manage.py migrate --fake-initial
python3 $homeDir/manage.py migrate
python3 $homeDir/manage.py makemigrations bodzify_api
python3 $homeDir/manage.py migrate
python3 $homeDir/manage.py loaddata initial_data