FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/nginx.conf

ENV LogDir=/var/log/nginx/
RUN ln -sf /dev/stdout {LogDir}access.log
RUN ln -sf /dev/stderr {LogDir}error.log
