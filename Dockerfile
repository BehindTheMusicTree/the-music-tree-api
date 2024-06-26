# syntax=docker/dockerfile:1

FROM python:3.11-buster

ARG DJANGO_LOG_DIR
ARG GUNICORN_LOG_DIR
ARG LIBRARIES_DIR
ARG TEMP_UPLOADED_FILES_DIR

RUN if [ -z "$DJANGO_LOG_DIR" ]; then echo "The DJANGO_LOG_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$GUNICORN_LOG_DIR" ]; then echo "The GUNICORN_LOG_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$LIBRARIES_DIR" ]; then echo "The LIBRARIES_DIR argument is not provided" >&2; exit 1; fi
RUN if [ -z "$TEMP_UPLOADED_FILES_DIR" ]; then echo "The TEMP_UPLOADED_FILES_DIR argument is not provided" >&2; exit 1; fi

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DockerHome=/home/app/webapp \
    LibrariesDir=$LIBRARIES_DIR \
    DjangoLogDir=$DJANGO_LOG_DIR \
    GunicornLogDir=$GUNICORN_LOG_DIR \
    TempUploadedFilesDir=$TEMP_UPLOADED_FILES_DIR

RUN apt-get update && \
    apt-get install -y gosu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p $DockerHome ${DockerHome}/staticfiles $LibrariesDir $DjangoLogDir $GunicornLogDir $TempUploadedFilesDir && \
    touch ${DjangoLogDir}requests.log \
    ${DjangoLogDir}requests.debug.log \
    ${DjangoLogDir}general.log \
    ${DjangoLogDir}info.log \
    ${DjangoLogDir}django.log \
    ${DjangoLogDir}bodzify-api.log \
    ${GunicornLogDir}error.log \
    ${GunicornLogDir}access.log && \
    chmod 777 -R $LibrariesDir $DjangoLogDir $GunicornLogDir $TempUploadedFilesDir

COPY . $DockerHome

WORKDIR $DockerHome

RUN apt update && \
    apt install -y flac ffmpeg libchromaprint-tools && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    # The env packages could have been simply copied but the executables wouldn't have been added to the PATH.
    pip install -r requirements.txt

RUN pip list | grep gunicorn
RUN echo $PATH && which gunicorn