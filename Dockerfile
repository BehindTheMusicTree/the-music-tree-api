# syntax=docker/dockerfile:1

FROM python:3.11-buster 


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# To run gunicorn as a non-root user without password prompt
RUN apt-get update && apt-get install -y gosu

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

ENV DockerHome=/home/app/webapp
RUN mkdir -p $DockerHome
WORKDIR $DockerHome

COPY . $DockerHome

ENV MediaDir=/home/app/webapp/lib/bodzify-api/media
ENV LibrariesDir=${MediaDir}/libraries
ENV LogDir=/home/app/webapp/log/
ENV DjangoLogDir=${LogDir}django/
ENV GunicornLogDir=${LogDir}gunicorn/
ENV TempUploadedFilesDir=/tmp/bodzify-api/uploaded-files/

RUN mkdir -p ${DockerHome}/staticfiles $LibrariesDir $LogDir $DjangoLogDir $GunicornLogDir $TempUploadedFilesDir && \
    touch ${DjangoLogDir}requests.log \
    ${DjangoLogDir}requests.debug.log \
    ${DjangoLogDir}general.log \
    ${DjangoLogDir}info.log \
    ${DjangoLogDir}django.log \
    ${DjangoLogDir}bodzify-api.log \
    ${GunicornLogDir}error.log \
    ${GunicornLogDir}access.log && \
    chmod 777 -R $LibrariesDir $GunicornLogDir $TempUploadedFilesDir && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache && \
    apt update && \
    apt install -y flac ffmpeg libchromaprint-tools && \
    chown -R www-data:www-data /opt/bodzify-api && \
    python manage.py collectstatic --noinput