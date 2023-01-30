mediaDir=/var/lib/bodzify-api/media/

sudo mkdir -p $mediaDir
sudo chown $USER $mediaDir
sudo chmod 775 $mediaDir

djangoLogDir=/var/log/bodzify-api/

sudo mkdir -p $djangoLogDir
sudo chown $USER $djangoLogDir
sudo chmod 775 $djangoLogDir

gunicornLogDir=/var/log/bodzify-api/

sudo mkdir -p $gunicornLogDir
sudo chown $USER $gunicornLogDir
sudo chmod 775 $gunicornLogDir