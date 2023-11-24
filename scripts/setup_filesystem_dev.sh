mediaDir=/var/lib/bodzify-api/media/

sudo mkdir -p $mediaDir
sudo chmod 775 $mediaDir
sudo chown -R $USER $mediaDir

logDir=/var/log/bodzify-api/

sudo mkdir -p $logDir
sudo touch ${logDir}access.log
sudo touch ${logDir}general.log
sudo touch ${logDir}info.log
sudo touch ${logDir}django.log
sudo touch ${logDir}bodzify-api.log
sudo chown -R $USER $logDir
sudo chmod -R 775 $logDir

staticDir=/var/www/bodzify-api/static/

sudo mkdir -p $staticDir
sudo chmod 775 $staticDir
sudo chown -R $USER $staticDir