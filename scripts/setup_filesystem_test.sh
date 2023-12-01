#!/bin/bash

mediaDir=/var/lib/bodzify-api/media/
sudo mkdir -p $mediaDir
sudo chown bodzify $mediaDir
sudo chgrp bodzify $mediaDir
sudo chmod 775 $mediaDir

bodzifyApiLogDir=/var/log/bodzify-api/
sudo mkdir $bodzifyApiLogDir

webappLogDir=${bodzifyApiLogDir}webapp/
sudo mkdir $webappLogDir
sudo touch ${webappLogDir}access.log
sudo touch ${webappLogDir}general.log
sudo touch ${webappLogDir}info.log
sudo touch ${webappLogDir}django.log
sudo touch ${webappLogDir}bodzify-api.log

nginxLogDir=${bodzifyApiLogDir}nginx/
sudo mkdir $nginxLogDir
sudo touch ${nginxLogDir}access.log
sudo touch ${nginxLogDir}error.log

gunicornLogDir=${bodzifyApiLogDir}gunicorn/
sudo mkdir $gunicornLogDir
sudo touch ${gunicornLogDir}access.log
sudo touch ${gunicornLogDir}error.log

webhookLogDir=${bodzifyApiLogDir}webhook/
sudo mkdir $webhookLogDir
sudo touch ${webhookLogDir}redeploy.log

sudo chown -R bodzify:bodzify $bodzifyApiLogDir
sudo chmod -R 775 $bodzifyApiLogDir

webhookDir=/var/webhooks/
sudo mkdir $webhookDir
sudo chown bodzify:bodzify $webhookDir
sudo chmod 775 $webhookDir

webhookScriptsDir=${webhookDir}scripts/
sudo mkdir $webhookScriptsDir
sudo chown bodzify:bodzify $webhookScriptsDir
sudo chmod 775 $webhookScriptsDir

scriptsDir=/var/scripts/bodzify/
sudo mkdir $scriptsDir
sudo chown bodzify:bodzify $scriptsDir
sudo chmod 775 $scriptsDir

sslDir=/etc/ssl/bodzify/
sudo mkdir $sslDir
sudo chown bodzify:bodzify $sslDir
sudo chmod 775 $sslDir

staticDir=/var/www/bodzify-api/static/
sudo mkdir -p $staticDir
sudo chown -R bodzify:bodzify $staticDir
sudo chmod 775 $staticDir

nginxConfDir=/etc/nginx/
sudo mkdir $nginxConfDir
sudo chown -R bodzify:bodzify $nginxConfDir
sudo chmod 775 $nginxConfDir