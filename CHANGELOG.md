# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Replace audio metadata management module with audiometa-python 0.2.4
- Upgrade mutagen to 1.46.0 (from 1.45.0 required by audiometa-python)
- Note: psycopg2-binary 2.9.5 is not compatible with Python 3.13; requires Python 3.12 or earlier, or a newer version of psycopg2-binary

## [v0.2.0] - 2025-04-03

### Added
- Enable Spotify integration with comprehensive API support:
  - Track search and lookup by ID/ISRC
  - Artist information retrieval
  - Audio features analysis (tempo, key, energy, danceability)
  - Spotify OAuth authentication for user accounts
  - Track preview URL support
  - Album information integration
  - Artist popularity and genre data

## [v0.1.3] - 2025-04-02

### Added
- Enable genre tree JSON import
- Enable genre tree JSON export
- Enavle delete criteria

### Changed
- Arrays in JSON must be without [] and in multipart with []

## [v0.1.2] - 2025-03-11

### Added
- Enable track archiving
- Complete filtering for all list requests
- Handle more tags formats: ID3v1 (.mp3, .wav, .flac), RIFF (wav)
- Implement a complete and consistent error handling system with precise codes (validation codes for bad requests)

### Changed
- Put all test files in same directory with consistent naming
- Set app not to handle in memory files: small files are handle as regular files

## [v0.1.1] - 2024-09-06

### Added

- Fingerprint check