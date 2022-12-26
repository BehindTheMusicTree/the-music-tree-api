# syntax=docker/dockerfile:1

# copy source and install dependencies
FROM python:3.10-buster 

ARG secretKey
ARG djangoDev
ARG djangoProd
ENV SECRET_KEY=$secretKey
ENV DJANGO_DEV=$djangoDev
ENV DJANGO_PROD=$djangoProd
# ENV DB_DATABASE=dbDatabase
# ENV DB_USERNAME
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT'),
# ENV DB_PASSWORD=185.224.139.218

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
CMD gunicorn --certfile=ssl/www.bodzify.com.chained.crt --keyfile=ssl/www.bodzify.com.key --bind 0.0.0.0:443 -k uvicorn.workers.UvicornWorker bodzify_api.asgi:application