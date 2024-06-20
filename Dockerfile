# syntax=docker/dockerfile:1

FROM python:3.11-buster 

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DockerHome=/home/app/webapp \
    MediaDir=/home/app/webapp/lib/bodzify-api/media \
    LibrariesDir=${MediaDir}/libraries \
    LogDir=/home/app/webapp/log/ \
    DjangoLogDir=${LogDir}django/ \
    GunicornLogDir=${LogDir}gunicorn/ \
    TempUploadedFilesDir=/tmp/bodzify-api/uploaded-files/

RUN apt-get update && \
    apt-get install -y gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p $DockerHome \
    ${DockerHome}/staticfiles \
    $LibrariesDir \
    $LogDir \
    $DjangoLogDir \
    $GunicornLogDir \
    $TempUploadedFilesDir && \
    touch ${DjangoLogDir}requests.log \
    ${DjangoLogDir}requests.debug.log \
    ${DjangoLogDir}general.log \
    ${DjangoLogDir}info.log \
    ${DjangoLogDir}django.log \
    ${DjangoLogDir}bodzify-api.log \
    ${GunicornLogDir}error.log \
    ${GunicornLogDir}access.log && \
    chmod 777 -R $LibrariesDir $GunicornLogDir $TempUploadedFilesDir

COPY . $DockerHome

RUN apt update && \
    apt install -y flac ffmpeg libchromaprint-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*