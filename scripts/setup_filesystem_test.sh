mediaDir=/var/lib/bodzify-api/media/

sudo mkdir -p $mediaDir
sudo chown bodzify $mediaDir
sudo chmod 775 $mediaDir

logDir=/var/log/bodzify-api/

sudo mkdir -p $logDir
sudo chown bodzify $logDir
sudo chmod 775 $logDir