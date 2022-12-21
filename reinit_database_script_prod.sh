sudo -u postgres dropdb -e bodzify_api -f
sudo -u postgres -H -- psql -c "create database bodzify_api with owner django;"
sudo rm -r /var/www/html/bodzify-api/media/libraries/*
python3 /var/www/html/bodzify-api//manage.py clear_cache
python3 /var/www/html/bodzify-api//manage.py clean_pyc
python3 /var/www/html/bodzify-api//manage.py reset_schema
python3 /var/www/html/bodzify-api//manage.py reset_db
sudo rm -r /var/www/html/bodzify-api/bodzify_api/migrations
python3 /var/www/html/bodzify-api/manage.py makemigrations
python3 /var/www/html/bodzify-api/manage.py makemigrations bodzify_api
python3 /var/www/html/bodzify-api/manage.py migrate
python3 /var/www/html/bodzify-api/manage.py runserver
