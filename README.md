# Bodzify API

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.2-green.svg)](https://www.djangoproject.com/)

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

### Developer environment (recommended)

To keep a consistent, reproducible development environment across contributors, we recommend creating a workspace-local virtual environment named `.venv` in the project root and pointing Visual Studio Code to use that interpreter.

1) Create a `.venv` in the project root:

```bash
python3 -m venv .venv
```

2) Activate the virtualenv:

- macOS / Linux:
	```bash
	source .venv/bin/activate
	```
- Windows (PowerShell):
	```powershell
	.\.venv\Scripts\Activate.ps1
	```

3) Install dependencies:
```bash
pip install -r requirements.txt
```

4) VS Code setup
- The repository workspace settings now reference `${workspaceFolder}/.venv/bin/python` (instead of a machine-local absolute path) so VS Code will automatically pick the correct interpreter if your `.venv` is in the project root.
- Alternatively, run the VS Code command `Python: Select Interpreter` and choose `.venv/bin/python`.

If you prefer a different venv name or layout, adjust your local VS Code interpreter selection. The repository stores a workspace-relative default to keep experience consistent for new contributors.

## Audio Metadata Handling
The Bodzify API uses [`audiometa-python`](https://github.com/your-username/audiometa-python) for reading and writing audio metadata. The implementation is format-agnostic and handles multiple metadata formats (ID3v1, ID3v2, Vorbis, RIFF) automatically. For more details, see the [Audio Metadata Handling documentation](bodzify_api/utils/audiometa_adapter/README.md).

## MusicBrainz Integration
The Bodzify API integrates with MusicBrainz through the AcoustID fingerprinting service to automatically identify audio tracks and retrieve metadata such as title, artist, and release date. Audio files are fingerprinted using Chromaprint and matched against the MusicBrainz database. For more details, see the [MusicBrainz Integration documentation](bodzify_api/utils/musicbrainz/README.md).

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
