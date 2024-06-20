#!/bin/bash

SCRIPTS_DIR=$(dirname "$0")/

# Load environment variables in the current shell
source "${SCRIPTS_DIR}load_env_variables.sh"

mediaDir=/var/lib/bodzify-api/media/
sudo mkdir -p $mediaDir
sudo chmod 775 $mediaDir
sudo chown -R $USER $mediaDir

tempUploadedFilesDir=/tmp/bodzify-api/uploaded-files/
sudo mkdir -p $tempUploadedFilesDir
sudo chmod 775 $tempUploadedFilesDir
sudo chown -R $USER $tempUploadedFilesDir

if [ -z "$LOG_DIR" ]
then
    djangoLogDir=$SCRIPTS_DIR../
else
    djangoLogDir=$LOG_DIR
fi

sudo mkdir -p $djangoLogDir
sudo touch ${djangoLogDir}requests.log
sudo touch ${djangoLogDir}requests.debug.log
sudo touch ${djangoLogDir}exceptions.log
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