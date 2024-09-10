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
You need to set up several environment variables for development, build, and run. Below are the required variables and examples of how to set them.

#### Development
Create a copy of the file env/.env.development.example here: env/.env and set the values.

#### Build
Create a .env.build file in the root directory with the following content:

#### Run
Create a .env file in the root directory with the following content:

## Usage
TODO

## API Endpoints
TODO

## License
This project is licensed under the MIT License.

## Acknowledgements
This project use acoustid to fingerprint the audio files in order to identify each track.