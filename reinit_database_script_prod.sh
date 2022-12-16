sudo -u postgres dropdb -e bodzify_api -f
sudo -u postgres -H -- psql -c "create database bodzify_api with owner django;"
sudo rm -r /var/www/html/bodzify-api/bodzify_api/migrations
sudo rm -r /var/www/html/bodzify-api/media/libraries/*
python3 /var/www/html/bodzify-api/manage.py migrate
python3 /var/www/html/bodzify-api/manage.py migrate --fake
python3 /var/www/html/bodzify-api/manage.py makemigrations 
python3 /var/www/html/bodzify-api/manage.py migrate --fake-initial
python3 /var/www/html/bodzify-api/manage.py migrate
python3 /var/www/html/bodzify-api/manage.py makemigrations bodzify_api
python3 /var/www/html/bodzify-api/manage.py loaddata initial_data
python3 /var/www/html/bodzify-api/manage.py runserver
