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
sudo touch ${logDir}django.log
sudo touch ${logDir}bodzify-api.log
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

nginxLogAccessFile=/var/log/nginx/access.log
sudo touch $nginxLogAccessFile
sudo chmod 775 $nginxLogAccessFile
sudo chown -R bodzify $nginxLogAccessFile
sudo chgrp -R bodzify $nginxLogAccessFile

nginxLogErrorFile=/var/log/nginx/error.log
sudo touch $nginxLogErrorFile
sudo chmod 775 $nginxLogErrorFile
sudo chown -R bodzify $nginxLogErrorFile
sudo chgrp -R bodzify $nginxLogErrorFile

gunicornLogDir=/var/log/gunicorn/
sudo mkdir -p $gunicornLogDir
sudo touch ${gunicornLogDir}access.log
sudo touch ${gunicornLogDir}error.log
sudo chmod 775 $gunicornLogDir
sudo chown -R bodzify:bodzify $gunicornLogDir

webhookLogDir=/var/log/webhook/
sudo mkdir -p $webhookLogDir
sudo chmod 775 $webhookLogDir
sudo chown -R bodzify $webhookLogDir
sudo chgrp -R bodzify $webhookLogDir

webhookLogFile=${webhookLogDir}general.log
sudo touch $webhookLogFile
sudo chmod 775 $webhookLogFile
sudo chown -R bodzify $webhookLogFile
sudo chgrp -R bodzify $webhookLogFile

redeployLogFile=${webhookLogDir}redeploy.log
sudo touch $redeployLogFile
sudo chmod 775 $redeployLogFile
sudo chown -R bodzify $redeployLogFile
sudo chgrp -R bodzify $redeployLogFile