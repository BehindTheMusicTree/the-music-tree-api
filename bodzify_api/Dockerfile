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

ENV DockerHome=/home/app/webapp
ENV LogDir=/var/log/bodzify-api/
ENV AccessLog=$LogDir/access.log
ENV GeneralLog=$LogDir/general.log
ENV InfoLog=$LogDir/info.log
ENV DjangoLog=$LogDir/django.log
ENV BodzifyApiLog=$LogDir/bodzify-api.log

ENV GunicornLogDir=/var/log/gunicorn/
ENV GunicornAccessLog=$GunicornLogDir/access.log
ENV GunicornErrorLog=$GunicornLogDir/error.log

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/bash --uid 1000 bodzify

# Copy source and install dependencies
RUN mkdir -p $DockerHome
WORKDIR $DockerHome

COPY . $DockerHome

RUN mkdir -p $LogDir
RUN touch $AccessLog
RUN touch $GeneralLog
RUN touch $InfoLog
RUN touch $DjangoLog
RUN touch $BodzifyApiLog

RUN mkdir -p $GunicornLogDir
RUN touch $GunicornAccessLog
RUN touch $GunicornErrorLog
RUN chown -R bodzify:bodzify $GunicornLogDir

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache
RUN chown -R www-data:www-data /opt/bodzify-api
# RUN python manage.py collectstatic --noinput