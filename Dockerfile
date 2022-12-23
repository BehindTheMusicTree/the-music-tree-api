# syntax=docker/dockerfile:1

# copy source and install dependencies
FROM python:3.10-buster 

ARG secretKey
ENV SECRET_KEY=$secretKey

ENV DockerHome=/home/app/webapp

RUN mkdir -p $DockerHome
WORKDIR $DockerHome  
COPY . $DockerHome  

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache
RUN chown -R www-data:www-data /opt/bodzify-api

# start server
EXPOSE 443
STOPSIGNAL SIGTERM
RUN export SECRET_KEY=$secretKey
RUN gunicorn --certfile=ssl/www.bodzify.com.chained.crt --keyfile=<ssl/www.bodzify.com.key --bind 0.0.0.0:443 -k uvicorn.workers.UvicornWorker bodzify_api.asgi:application