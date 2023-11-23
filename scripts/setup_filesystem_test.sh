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

scriptsDir=/var/scripts/bodzify/
sudo mkdir -p $scriptsDir
sudo chown bodzify $scriptsDir
sudo chgrp bodzify $scriptsDir
sudo chmod 775 $scriptsDir

sslDir=/etc/ssl/bodzify/
sudo mkdir -p $sslDir
sudo chown bodzify $sslDir
sudo chgrp bodzify $sslDir
sudo chmod 775 $sslDir

staticDir=/var/www/bodzify-api/static/

sudo mkdir -p $staticDir
sudo chmod 775 $staticDir
sudo chown -R bodzify $staticDir
sudo chgrp -R bodzify $staticDir

webappDir=/var/www/bodzify-api/webapp/

sudo mkdir -p $webappDir
sudo chmod 775 $webappDir
sudo chown -R bodzify $webappDir
sudo chgrp -R bodzify $webappDir

nginxConfDir=/etc/nginx/

sudo mkdir -p $nginxConfDir
sudo chmod 775 $nginxConfDir
sudo chown -R bodzify $nginxConfDir
sudo chgrp -R bodzify $nginxConfDir

