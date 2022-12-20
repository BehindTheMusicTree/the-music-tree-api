# syntax=docker/dockerfile:1

# copy source and install dependencies
FROM python:3.10-buster
RUN mkdir -p /opt/bodzify-api
RUN mkdir -p /opt/bodzify-api/pip_cache
RUN mkdir -p /opt/bodzify-api/bodzify_api
COPY requirements.txt start-server.sh /opt/bodzify-api/
COPY bodzify_api /opt/bodzify-api/bodzify_api/
WORKDIR /opt/bodzify-api
RUN pip install -r requirements.txt --cache-dir /opt/bodzify-api/pip_cache
RUN chown -R www-data:www-data /opt/bodzify-api

# start server
EXPOSE 443
STOPSIGNAL SIGTERM
CMD ["/opt/bodzify-api/start-server.sh"]