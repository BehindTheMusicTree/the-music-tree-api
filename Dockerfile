# syntax=docker/dockerfile:1

FROM python:3.11-buster

ARG DJANGO_LOG_DIR
ARG GUNICORN_LOG_DIR
ARG LIBRARIES_DIR
ARG TMP_UPLOADED_FILES_DIR
ARG STATIC_FILES_DIR

RUN if [ -z "$DJANGO_LOG_DIR" ]; then echo "The DJANGO_LOG_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$GUNICORN_LOG_DIR" ]; then echo "The GUNICORN_LOG_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$LIBRARIES_DIR" ]; then echo "The LIBRARIES_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$TMP_UPLOADED_FILES_DIR" ]; then echo "The TMP_UPLOADED_FILES_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$STATIC_FILES_DIR" ]; then echo "The STATIC_FILES_DIR argument is not provided" >&2; exit 1; fi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_HOME=/home/app/webapp \
    LOBRARIES_DIR=$LIBRARIES_DIR \
    DJANGO_LOG_DIR=$DJANGO_LOG_DIR \
    GUNICORN_LOG_DIR=$GUNICORN_LOG_DIR \
    TMP_UPLOADED_FILES_DIR=$TMP_UPLOADED_FILES_DIR \
    STATIC_FILES_DIR=$STATIC_FILES_DIR

RUN apt-get update && \
    apt-get install -y gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p $DOCKER_HOME $LOBRARIES_DIR $DJANGO_LOG_DIR $GUNICORN_LOG_DIR $TMP_UPLOADED_FILES_DIR $STATIC_FILES_DIR && \
    touch ${DJANGO_LOG_DIR}requests.log \
    ${DJANGO_LOG_DIR}requests.debug.log \
    ${DJANGO_LOG_DIR}general.log \
    ${DJANGO_LOG_DIR}info.log \
    ${DJANGO_LOG_DIR}django.log \
    ${DJANGO_LOG_DIR}bodzify-api.log \
    ${GUNICORN_LOG_DIR}error.log \
    ${GUNICORN_LOG_DIR}access.log && \
    chmod 777 -R $LOBRARIES_DIR $DJANGO_LOG_DIR $GUNICORN_LOG_DIR $TMP_UPLOADED_FILES_DIR

COPY . $DOCKER_HOME

WORKDIR $DOCKER_HOME

RUN apt update && \
    apt install -y flac ffmpeg libchromaprint-tools jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    # The env packages could have been simply copied but the executables wouldn't have been added to the PATH.
    pip install -r requirements.txt

RUN pip list | grep gunicorn
RUN echo $PATH && which gunicorn