mediaDir=/var/lib/bodzify-api/media/

sudo mkdir -p $mediaDir
sudo chown bodzify $mediaDir
sudo chgrp bodzify $mediaDir
sudo chmod 775 $mediaDir

logDir=/var/log/bodzify-api/

sudo mkdir -p $logDir
sudo touch ${logDir}access.log
sudo touch ${logDir}general.log
sudo touch ${logDir}info.log
sudo chown -R bodzify $logDir
sudo chgrp -R bodzify $logDir
sudo chmod 775 $logDir

webhookDir=/var/webhooks/

sudo mkdir -p $webhookDir
sudo chown bodzify $webhookDir
sudo chgrp bodzify $webhookDir
sudo chmod 775 $webhookDir

webhookScriptsDir=${webhookDir}scripts/

sudo mkdir -p $webhookScriptsDir
sudo chown bodzify $webhookScriptsDir
sudo chgrp bodzify $webhookScriptsDir
sudo chmod 775 $webhookScriptsDir