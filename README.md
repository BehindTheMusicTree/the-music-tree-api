# Bodzify API

Bodzify API is an online platform similar to iTunes, designed for managing and interacting with music tracks. It offers a range of features to help you organize, tag, and rate your music, as well as create automatic hierarchical genre playlists.

## Features

- **Upload Tracks**: Easily upload your music tracks to the platform.
- **Tag Tracks**: Tag your tracks with metadata such as artist names, album titles, and more. This tagging process helps organize your music files.
- **Rate Tracks**: Users can rate tracks, providing a way to highlight popular or preferred songs.
- **Create Genre Hierarchies**: The most important feature of Bodzify API is the ability to create a hierarchy of music genres. For example, if a track is tagged as "techno," it will automatically be included in both the "techno" playlist and the broader "electronic music" playlist.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mignot/bodzify-api-django.git
   cd bodzify-api

### Environment Variables
You need to set up several environment variables for development, build, and run. Below are the required variables and 
examples of how to set them.

#### Development
Create a copy of the file env/.env.development.example here: env/.env and set the values.

#### Build
The docker build requires the following environment variables:
- `APP_NAME`
- `APP_VERSION`
- `TMP_UPLOADED_FILES_DIR`
- `MEDIA_DIR`
- `LIBRARIES_DIR_NAME`
- `STATIC_FILES_DIR`
- `STATIC_FILES_DEFAULT_INTERNAL_DIR`
- `DJANGO_LOG_DIR`
- `DJANGO_LOG_GENERAL_FILENAME`
- `DJANGO_LOG_INFO_FILENAME`
- `DJANGO_LOG_REQUESTS_FILENAME`
- `DJANGO_LOG_REQUESTS_DEBUG_FILENAME`
- `DJANGO_LOG_EXCEPTIONS_FILENAME`
- `DJANGO_LOG_DJANGO_FILENAME`
- `DJANGO_LOG_APP_FILENAME`
- `GUNICORN_LOG_DIR`
- `GUNICORN_LOG_ERROR_FILENAME`
- `GUNICORN_LOG_ACCESS_FILENAME`

#### Running the container
Running the container requires the following environment variables:
- `DJANGO_SECRET_KEY`
- `ACOUSTID_API_KEY`
- `CSRF_TRUSTED_ORIGINS`
- `ALLOWED_HOSTS`
- `DB_BODZIFY_API_DB_NAME`
- `DB_BODZIFY_API_USERNAME`
- `DB_BODZIFY_API_USER_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `AFP_CONTAINER_NAME` (AFP meaning Audio FingerPrinter)
- `AFP_PORT`
- `AFP_POST_ENDPOINT`

## Database Requirement
The Bodzify API requires a database to function. It has been tested with PostgreSQL, and it is recommended to use PostgreSQL for the best compatibility and performance.

## Audio Meta Analyse Requirement
For audio meta analysis, the Bodzify API requires an app called Audio Fingerprinter. You can find the Audio Fingerprinter app on GitHub at the following link: [Audio Fingerprinter](https://github.com/Bodzify/bodzify-audio-fingerprinter-flask)

## Usage
TODO

## API Endpoints
TODO

## License
This project is licensed under the MIT License.

## Acknowledgements
This project use acoustid to fingerprint the audio files in order to identify each track.