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

RUN groupadd -g 1003 bodzify && useradd -u 1002 -g bodzify bodzify

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

RUN mkdir ${DockerHome}/staticfiles

ENV MediaDir=/var/lib/bodzify-api/media
ENV LibrariesDir=${MediaDir}/libraries
RUN mkdir -p $LibrariesDir
RUN chmod -R 755 $MediaDir
RUN chown -R bodzify:bodzify $MediaDir

ENV LogDir=/var/log/
RUN mkdir -p $LogDir

ENV DjangoLogDir=${LogDir}django/

RUN mkdir $DjangoLogDir
RUN touch ${DjangoLogDir}requests.log
RUN touch ${DjangoLogDir}requests.debug.log
RUN touch ${DjangoLogDir}general.log
RUN touch ${DjangoLogDir}info.log
RUN touch ${DjangoLogDir}django.log
RUN touch ${DjangoLogDir}bodzify-api.log
RUN chmod -R 755 $DjangoLogDir
RUN chown -R bodzify:bodzify $DjangoLogDir

ENV GunicornLogDir=/home/app/logs/gunicorn/
RUN mkdir -p $GunicornLogDir
RUN touch ${GunicornLogDir}error.log
RUN chmod -R 777 $GunicornLogDir
RUN chown -R bodzify:bodzify $GunicornLogDir

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache
RUN chown -R www-data:www-data /opt/bodzify-api
RUN python manage.py collectstatic --noinput

USER bodzify
