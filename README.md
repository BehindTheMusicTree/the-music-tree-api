# Bodzify API

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.0-green.svg)](https://www.djangoproject.com/)

Bodzify API is an online platform similar to iTunes, designed for managing and interacting with music tracks. It offers a range of features to help you organize, tag, and rate your music, as well as create automatic hierarchical genre playlists.

## Features

- **Upload Tracks**: Easily upload your music tracks to the platform.
- **Tag Tracks**: Tag your tracks with metadata such as artist names, album titles, and more. This tagging process helps organize your music files.
- **Rate Tracks**: Users can rate tracks, providing a way to highlight popular or preferred songs.
- **Create Genre Hierarchies**: The most important feature of Bodzify API is the ability to create a hierarchy of music genres. For example, if a track is tagged as "techno," it will automatically be included in both the "techno" playlist and the broader "electronic music" playlist.

## Getting Started

For detailed setup and installation instructions, please see the [Contributing Guidelines](CONTRIBUTING.md#1-environment-setup).

**Quick Start:**
- Python 3.14
- Docker and Docker Compose
- PostgreSQL database
- See [CONTRIBUTING.md](CONTRIBUTING.md) for full setup instructions

## Audio Metadata Handling
The Bodzify API uses [`audiometa-python`](https://github.com/your-username/audiometa-python) for reading and writing audio metadata. The implementation is format-agnostic and handles multiple metadata formats (ID3v1, ID3v2, Vorbis, RIFF) automatically. For more details, see the [Audio Metadata Handling documentation](bodzify_api/utils/audiometa_adapter/README.md).

## Usage
TODO

## API Endpoints
TODO

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
This project use acoustid to fingerprint the audio files in order to identify each track.
Please visit [Acoustid Web Service](https://acoustid.org/webservice).
