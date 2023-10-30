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
ENV LogDir=$DockerHome/log
ENV AccessLogPath=$LogDir/access.log

# Copy source and install dependencies
RUN mkdir -p $DockerHome
WORKDIR $DockerHome  
COPY . $DockerHome
RUN mkdir -p $LogDir
RUN touch $AccessLogPath

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache
RUN chown -R www-data:www-data /opt/bodzify-api

RUN python manage.py collectstatic --noinput

# Start server
EXPOSE 443
STOPSIGNAL SIGTERM
CMD gunicorn --certfile=/etc/ssl/bodzify/www_bodzify_com.crt --keyfile=/etc/ssl/bodzify/www.bodzify.com.key --bind 0.0.0.0:443 -k uvicorn.workers.UvicornWorker bodzify_api.asgi:application