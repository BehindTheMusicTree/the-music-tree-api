mediaDir=/var/lib/bodzify-api/media/

sudo mkdir -p $mediaDir
sudo chmod 775 $mediaDir

sudo chown -R $USER $mediaDir

logDir=/var/log/bodzify-api/

sudo mkdir -p $logDir
sudo touch ${logDir}access.log
sudo touch ${logDir}general.log
sudo touch ${logDir}info.log
sudo chmod -R 775 $logDir

