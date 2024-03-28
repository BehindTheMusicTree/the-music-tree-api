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

ENV StaticfilesDir=${DockerHome}/staticfiles

ENV MediaDir=/var/lib/bodzify-api/media
ENV LibrariesDir=${MediaDir}/libraries

ENV LogDir=/var/log/

ENV DjangoLogDir=${LogDir}django/
ENV DjangoRequestsLog=${DjangoLogDir}requests.log
ENV DjangoRequestsDebugLog=${DjangoLogDir}requests.debug.log
ENV DjangoGeneralLog=${DjangoLogDir}general.log
ENV DjangoInfoLog=${DjangoLogDir}info.log
ENV DjangoDjangoLog=${DjangoLogDir}django.log
ENV DjangoBodzifyApiLog=${DjangoLogDir}bodzify-api.log

ENV GunicornLogDir=${LogDir}gunicorn/
ENV GunicornErrorLog=${GunicornLogDir}error.log

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN mkdir -p $DockerHome
WORKDIR $DockerHome

COPY . $DockerHome

RUN mkdir $StaticfilesDir
RUN mkdir -p $LibrariesDir

RUN chmod -R 755 $MediaDir
RUN chown -R 100000:100000 $MediaDir

RUN mkdir -p $LogDir

RUN mkdir $DjangoLogDir
RUN touch $DjangoRequestsLog
RUN touch $DjangoRequestsDebugLog
RUN touch $DjangoGeneralLog
RUN touch $DjangoInfoLog
RUN touch $DjangoDjangoLog
RUN touch $DjangoBodzifyApiLog

RUN mkdir $GunicornLogDir
RUN touch $GunicornErrorLog

RUN chmod -R 755 $LogDir
RUN chown -R 100000:100000 $LogDir

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache
RUN chown -R www-data:www-data /opt/bodzify-api
RUN python manage.py collectstatic --noinput