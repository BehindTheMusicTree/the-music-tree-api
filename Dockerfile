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
ENV LogDir=/var/log/

ENV DjangoLogDir=${LogDir}django/
ENV DjangoAccessLog=${DjangoLogDir}access.log
ENV DjangoGeneralLog=${DjangoLogDir}general.log
ENV DjangoInfoLog=${DjangoLogDir}info.log
ENV DjangoDjangoLog=${DjangoLogDir}django.log
ENV DjangoBodzifyApiLog=${DjangoLogDir}bodzify-api.log

ENV GunicornLogDir=${LogDir}gunicorn/
ENV GunicornAccessLog=${GunicornLogDir}access.log
ENV GunicornErrorLog=${GunicornLogDir}error.log

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $DockerHome
WORKDIR $DockerHome

COPY . $DockerHome

RUN mkdir -p $LogDir

RUN mkdir $DjangoLogDir
RUN touch $DjangoAccessLog
RUN touch $DjangoGeneralLog
RUN touch $DjangoInfoLog
RUN touch $DjangoDjangoLog
RUN touch $DjangoBodzifyApiLog

RUN mkdir $GunicornLogDir
RUN touch $GunicornAccessLog
RUN touch $GunicornErrorLog

RUN chmod -R 755 $LogDir
RUN chown -R 100000:100000 $LogDir

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache
RUN chown -R www-data:www-data /opt/bodzify-api
RUN python manage.py collectstatic --noinput