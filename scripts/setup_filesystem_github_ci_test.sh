#!/bin/bash

mediaDir=/var/lib/bodzify-api/media/
sudo mkdir -p $mediaDir
sudo chown $USER $mediaDir
sudo chmod 775 $mediaDir

tempUploadedFilesDir=/tmp/bodzify-api/uploaded-files/
sudo mkdir -p $tempUploadedFilesDir
sudo chmod 775 $tempUploadedFilesDir
sudo chown -R $USER $tempUploadedFilesDir

logDir=/var/log/django/
sudo mkdir -p $logDir
sudo chown $USER $logDir
sudo chmod 775 $logDir