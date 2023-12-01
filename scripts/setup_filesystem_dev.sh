#!/bin/bash

mediaDir=/var/lib/bodzify-api/media/

sudo mkdir -p $mediaDir
sudo chmod 775 $mediaDir
sudo chown -R $USER $mediaDir

logDir=/var/log/bodzify-api/
sudo mkdir $logDir

djangoLogDir=${logDir}django/
sudo mkdir $djangoLogDir
sudo touch ${djangoLogDir}access.log
sudo touch ${djangoLogDir}general.log
sudo touch ${djangoLogDir}info.log
sudo touch ${djangoLogDir}django.log
sudo touch ${djangoLogDir}bodzify-api.log

sudo chmod -R 775 $djangoLogDir
sudo chown -R $USER $djangoLogDir

staticDir=/var/www/bodzify-api/static/

sudo mkdir -p $staticDir
sudo chmod 775 $staticDir
sudo chown -R $USER $staticDir