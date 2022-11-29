sudo -u postgres dropdb -e bodzify_api -f
sudo -u postgres -H -- psql -c "create database bodzify_api with owner django;"
sudo rm -r /var/www/html/bodzify-api/bodzify_api/migrations
sudo rm -r /var/www/html/bodzify-api/libraries/*
python3 /var/www/html/bodzify-api/manage.py migrate
python3 /var/www/html/bodzify-api/manage.py migrate --fake
python3 /var/www/html/bodzify-api/manage.py makemigrations 
python3 /var/www/html/bodzify-api/manage.py migrate --fake-initial
python3 /var/www/html/bodzify-api/manage.py migrate
python3 /var/www/html/bodzify-api/manage.py makemigrations bodzify_api
cp /var/www/html/bodzify-api/bodzify_api/migrations_initial_data/0002_populate.py /var/www/html/bodzify-api/bodzify_api/migrations/
python3 /var/www/html/bodzify-api/manage.py migrate
python3 /var/www/html/bodzify-api/manage.py createsuperuser --username admin --email admin@bodzify.com