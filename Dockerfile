# syntax=docker/dockerfile:1

FROM python:3.11-buster

ARG APP_IS_EXPOSED
ARG AUDIO_META_ANALYSE_IS_NEEDED
ARG TMP_UPLOADED_FILES_DIR
ARG MEDIA_DIR
ARG LIBRARIES_DIR_NAME
ARG STATIC_FILES_ARE_NEEDED
ARG STATIC_FILES_DIR
ARG STATIC_FILES_DEFAULT_INTERNAL_DIR
ARG DJANGO_LOGS_ARE_NEEDED
ARG DJANGO_LOG_DIR
ARG DJANGO_LOG_GENERAL_FILENAME
ARG DJANGO_LOG_INFO_FILENAME
ARG DJANGO_LOG_REQUESTS_FILENAME
ARG DJANGO_LOG_REQUESTS_DEBUG_FILENAME
ARG DJANGO_LOG_EXCEPTIONS_FILENAME
ARG DJANGO_LOG_DJANGO_FILENAME
ARG DJANGO_LOG_APP_FILENAME
ARG GUNICORN_LOG_DIR
ARG GUNICORN_LOG_ERROR_FILENAME
ARG GUNICORN_LOG_ACCESS_FILENAME

RUN if [ -z "$APP_IS_EXPOSED" ]; then echo "The APP_IS_EXPOSED argument is not provided" >&2; exit 1; fi
RUN if [ -z "$AUDIO_META_ANALYSE_IS_NEEDED" ]; then echo "The AUDIO_META_ANALYSE_IS_NEEDED argument is not provided" >&2; exit 1; fi
RUN if [ -z "$TMP_UPLOADED_FILES_DIR" ]; then echo "The TMP_UPLOADED_FILES_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$MEDIA_DIR" ]; then echo "The MEDIA_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$LIBRARIES_DIR_NAME" ]; then echo "The LIBRARIES_DIR_NAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$STATIC_FILES_ARE_NEEDED" ]; then echo "The STATIC_FILES_ARE_NEEDED argument is not provided" >&2; exit 1; fi
RUN if [ -z "$STATIC_FILES_DIR" ]; then echo "The STATIC_FILES_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$STATIC_FILES_DEFAULT_INTERNAL_DIR" ]; then echo "The STATIC_FILES_DEFAULT_INTERNAL_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOGS_ARE_NEEDED" ]; then echo "The DJANGO_LOGS_ARE_NEEDED argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_DIR" ]; then echo "The DJANGO_LOG_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_GENERAL_FILENAME" ]; then echo "The DJANGO_LOG_GENERAL_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_INFO_FILENAME" ]; then echo "The DJANGO_LOG_INFO_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_REQUESTS_FILENAME" ]; then echo "The DJANGO_LOG_REQUESTS_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_REQUESTS_DEBUG_FILENAME" ]; then echo "The DJANGO_LOG_REQUESTS_DEBUG_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_EXCEPTIONS_FILENAME" ]; then echo "The DJANGO_LOG_EXCEPTIONS_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_DJANGO_FILENAME" ]; then echo "The DJANGO_LOG_DJANGO_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$DJANGO_LOG_APP_FILENAME" ]; then echo "The DJANGO_LOG_APP_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$GUNICORN_LOG_DIR" ]; then echo "The GUNICORN_LOG_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$GUNICORN_LOG_ERROR_FILENAME" ]; then echo "The GUNICORN_LOG_ERROR_FILENAME argument is not provided" >&2; exit 1; fi
RUN if [ -z "$GUNICORN_LOG_ACCESS_FILENAME" ]; then echo "The GUNICORN_LOG_ACCESS_FILENAME argument is not provided" >&2; exit 1; fi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_HOME=/home/app/webapp \
    APP_IS_EXPOSED=$APP_IS_EXPOSED \
    AUDIO_META_ANALYSE_IS_NEEDED=$AUDIO_META_ANALYSE_IS_NEEDED \
    TMP_UPLOADED_FILES_DIR=$TMP_UPLOADED_FILES_DIR \
    MEDIA_DIR=$MEDIA_DIR \
    LIBRARIES_DIR_NAME=$LIBRARIES_DIR_NAME \
    STATIC_FILES_ARE_NEEDED=$STATIC_FILES_ARE_NEEDED \
    STATIC_FILES_DIR=$STATIC_FILES_DIR \
    STATIC_FILES_DEFAULT_INTERNAL_DIR=$STATIC_FILES_DEFAULT_INTERNAL_DIR \
    DJANGO_LOGS_ARE_NEEDED=$DJANGO_LOGS_ARE_NEEDED \
    DJANGO_LOG_DIR=$DJANGO_LOG_DIR \
    DJANGO_LOG_GENERAL_FILENAME=$DJANGO_LOG_GENERAL_FILENAME \
    DJANGO_LOG_INFO_FILENAME=$DJANGO_LOG_INFO_FILENAME \
    DJANGO_LOG_REQUESTS_FILENAME=$DJANGO_LOG_REQUESTS_FILENAME \
    DJANGO_LOG_REQUESTS_DEBUG_FILENAME=$DJANGO_LOG_REQUESTS_DEBUG_FILENAME \
    DJANGO_LOG_EXCEPTIONS_FILENAME=$DJANGO_LOG_EXCEPTIONS_FILENAME \
    DJANGO_LOG_DJANGO_FILENAME=$DJANGO_LOG_DJANGO_FILENAME \
    DJANGO_LOG_APP_FILENAME=$DJANGO_LOG_APP_FILENAME \
    GUNICORN_LOG_DIR=$GUNICORN_LOG_DIR \
    GUNICORN_LOG_ERROR_FILENAME=$GUNICORN_LOG_ERROR_FILENAME \
    GUNICORN_LOG_ACCESS_FILENAME=$GUNICORN_LOG_ACCESS_FILENAME

RUN apt-get update && \
    apt-get install -y gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . $DOCKER_HOME

WORKDIR $DOCKER_HOME

RUN apt update && \
    apt install -y flac ffmpeg libchromaprint-tools jq && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    # The env packages could have been simply copied but the executables wouldn't have been added to the PATH.
    pip install -r requirements.txt && \
    bash scripts/setup_filesystem.sh

RUN pip list | grep gunicorn
RUN echo $PATH && which gunicorn