FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

RUN useradd -ms /bin/bash bodzify

ENV LogDir=/var/log/nginx/
RUN mkdir -p $LogDir
RUN touch $LogDir/AccessLog
RUN touch $LogDir/ErrorLog
RUN chown -R bodzify:bodzify $LogDir
RUN chmod -R 775 $LogDir