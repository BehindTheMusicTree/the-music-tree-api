#!/bin/bash

mediaDir=/var/lib/bodzify-api/media/
sudo mkdir -p $mediaDir
sudo chown $USER $mediaDir
sudo chmod 775 $mediaDir

sharedDjangoTempUploadedFilesDir=/var/django_temp_uploaded_files/
sudo mkdir $sharedDjangoTempUploadedFilesDir
sudo chmod 775 $sharedDjangoTempUploadedFilesDir

logDir=/var/log/django/
sudo mkdir -p $logDir
sudo chown $USER $logDir
sudo chmod 775 $logDir