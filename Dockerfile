# syntax=docker/dockerfile:1

FROM python:3.11-buster 

ARG secretKey
ARG env
ARG dbUsername
ARG dbPassword
ARG dbDatabase
ARG dbHost
ARG dbPort

ENV SECRET_KEY=$secretKey
ENV ENV=$env
ENV DB_USERNAME=$dbUsername
ENV DB_PASSWORD=$dbPassword
ENV DB_DATABASE=$dbDatabase
ENV DB_HOST=$dbHost
ENV DB_PORT=$dbPort
ENV ACOUSTID_API_KEY=$acoustidApiKey


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

RUN mkdir ${DockerHome}/staticfiles && \
    mkdir -p $LibrariesDir && \
    mkdir -p $LogDir && \
    mkdir $DjangoLogDir && \
    touch ${DjangoLogDir}requests.log && \
    touch ${DjangoLogDir}requests.debug.log && \
    touch ${DjangoLogDir}general.log && \
    touch ${DjangoLogDir}info.log && \
    touch ${DjangoLogDir}django.log && \
    touch ${DjangoLogDir}bodzify-api.log && \
    mkdir -p $GunicornLogDir && \
    touch ${GunicornLogDir}error.log && \
    touch ${GunicornLogDir}access.log && \
    chmod 777 -R $LibrariesDir ${GunicornLogDir} && \
    pip install --upgrade pip && \
    pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache && \
    apt update && \
    apt install -y flac && \
    apt install -y ffpmeg && \
    apt install -y libchromaprint-tools && \
    chown -R www-data:www-data /opt/bodzify-api && \
    python manage.py collectstatic --noinput