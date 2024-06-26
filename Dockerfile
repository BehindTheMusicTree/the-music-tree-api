# syntax=docker/dockerfile:1

FROM python:3.11-buster 

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DockerHome=/home/app/webapp \
    MediaDir=/home/app/webapp/lib/bodzify-api/media/ \
    LogDir=/home/app/webapp/log/ \
    TempUploadedFilesDir=/tmp/bodzify-api/uploaded-files/

RUN echo "export LibrariesDir=${MediaDir}libraries/" >> /etc/profile && \
    echo "export DjangoLogDir=${LogDir}django/" >> /etc/profile && \
    echo "export GunicornLogDir=${LogDir}gunicorn/" >> /etc/profile

RUN apt-get update && \
    apt-get install -y gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p $DockerHome ${DockerHome}/staticfiles $LibrariesDir $DjangoLogDir $GunicornLogDir $TempUploadedFilesDir && \
    touch ${DjangoLogDir}requests.log \
    ${DjangoLogDir}requests.debug.log \
    ${DjangoLogDir}general.log \
    ${DjangoLogDir}info.log \
    ${DjangoLogDir}django.log \
    ${DjangoLogDir}bodzify-api.log \
    ${GunicornLogDir}error.log \
    ${GunicornLogDir}access.log && \
    chmod 777 -R $LibrariesDir $DjangoLogDir $GunicornLogDir $TempUploadedFilesDir

COPY . $DockerHome

WORKDIR $DockerHome

RUN apt update && \
    apt install -y flac ffmpeg libchromaprint-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    # The env packages could have been simply copied but the executables wouldn't have been added to the PATH.
    pip install -r requirements.txt

RUN pip list | grep gunicorn
RUN echo $PATH && which gunicorn