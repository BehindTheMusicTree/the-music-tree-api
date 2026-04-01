# TheMusicTreeAPI

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)

TheMusicTreeAPI is the API companion to [GrowTheMusicTree](https://github.com/BehindTheMusicTree/grow-the-music-tree-frontend), giving developers, researchers, and music platforms access to the full genre hierarchy, detailed metadata, and intelligent genre detection. Built with Django REST Framework and PostgreSQL, it enables personalized user profiling based on listening habits, delivers accurate track and artist classifications, and provides data-driven recommendations.

Perfect for powering music discovery, streaming personalization, event recommendations, and listener analytics, TheMusicTreeAPI brings the intelligence of the genre tree to any app or service.

For more information about the project's vision, goals, and technical approach, see [VISION.md](VISION.md).

## Table of Contents

- [Features](#features)
  - [Genre Hierarchy Access](#genre-hierarchy-access)
  - [Intelligent Classification](#intelligent-classification)
  - [User Profiling & Recommendations](#user-profiling--recommendations)
  - [API Access](#api-access)
- [Getting Started](#getting-started)
  - [VS Code Setup](#vs-code-setup)
- [Ecosystem](#ecosystem)
- [Usage](#usage)
  - [Base URL](#base-url)
  - [Authentication](#authentication)
    - [Obtaining a Token](#obtaining-a-token)
    - [Using the Token](#using-the-token)
    - [Refreshing a Token](#refreshing-a-token)
    - [Spotify Authentication](#spotify-authentication)
  - [Request Format](#request-format)
  - [Response Format](#response-format)
  - [Pagination](#pagination)
  - [Error Handling](#error-handling)
  - [Example: Uploading a Track](#example-uploading-a-track)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication-1)
  - [Users](#users)
  - [Library - Tracks](#library---tracks)
  - [Artists](#artists)
  - [Albums](#albums)
  - [Genres & Tags](#genres--tags)
  - [Playlists](#playlists)
  - [Plays](#plays)
  - [Search](#search)
  - [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

### Genre Hierarchy Access
- **Full Genre Tree**: Complete access to the hierarchical genre structure from GrowTheMusicTree
- **Genre Metadata**: Detailed metadata for genres, subgenres, and microgenres
- **Tree Navigation**: Query and explore the genre tree structure programmatically

### Intelligent Classification
- **Track Classification**: Accurate genre detection and classification for any track
- **Artist Classification**: Genre-based artist categorization and profiling
- **Intelligent Detection**: Classify tracks even outside mainstream genres

### User Profiling & Recommendations
- **Listening Habit Analysis**: Personalized user profiling based on listening patterns
- **Data-Driven Recommendations**: Recommendations powered by genre intelligence
- **Personalized Journeys**: Map user listening habits within the genre tree

### API Access
- **RESTful Endpoints**: Clean, intuitive API for developers and researchers
- **Comprehensive Documentation**: Complete API documentation and developer guides
- **Integration Ready**: Designed for easy integration into music platforms and services

## Getting Started

For detailed setup and installation instructions, please see the [Contributing Guidelines](CONTRIBUTING.md#1-environment-setup).

**Quick Start:**
- Python 3.14
- Docker and Docker Compose
- PostgreSQL database
- See [CONTRIBUTING.md](CONTRIBUTING.md) for full setup instructions

### VS Code Setup

The repository workspace settings reference `${workspaceFolder}/.venv/bin/python` (instead of a machine-local absolute path) so VS Code will automatically pick the correct interpreter if your `.venv` is in the project root.

Alternatively, run the VS Code command `Python: Select Interpreter` and choose `.venv/bin/python`.

If you prefer a different venv name or layout, adjust your local VS Code interpreter selection. The repository stores a workspace-relative default to keep experience consistent for new contributors.

## Ecosystem

Built inside the **[BehindTheMusicTree](https://github.com/BehindTheMusicTree)** ecosystem.

Want the big picture? Explore the full project universe on **[themusictree.org](https://themusictree.org)**, and see where this API fits on **[TheMusicTreeAPI](https://themusictree.org/projects/the-music-tree-api)**.

The portfolio website content lives in **[the-music-tree-frontend](https://github.com/BehindTheMusicTree/the-music-tree-frontend)**; this README focuses on building, testing, deploying, and contributing to this API. The web app for the genre tree is **[grow-the-music-tree-frontend](https://github.com/BehindTheMusicTree/grow-the-music-tree-frontend)**.

## Usage

### Base URL

All API endpoints are prefixed with the API version. The base URL format is:

```
/api/{version}/
```

For example: `/api/v0.2.0/`

### Authentication

The API uses JWT (JSON Web Tokens) for authentication. All endpoints require authentication unless otherwise specified.

#### Obtaining a Token

To authenticate, send a POST request to the token endpoint with your credentials:

```bash
POST /api/{version}/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Using the Token

Include the access token in the `Authorization` header for all authenticated requests:

```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

#### Refreshing a Token

When the access token expires, use the refresh token to obtain a new access token:

```bash
POST /api/{version}/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Spotify Authentication

The API also supports Spotify OAuth authentication:

```bash
GET /api/{version}/auth/spotify/
```

This initiates the Spotify OAuth flow for users who want to connect their Spotify account.

### Request Format

The API accepts requests in multiple formats:

- **JSON**: `Content-Type: application/json`
- **Multipart Form Data**: `Content-Type: multipart/form-data` (for file uploads)
- **Form URL Encoded**: `Content-Type: application/x-www-form-urlencoded`

**Note:** For multipart requests with list fields, use the `[]` suffix (e.g., `artists_names[]`). JSON requests can use standard array notation.

### Response Format

All responses are returned in camelCase JSON format. The API uses standard HTTP status codes:

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Validation error or invalid input
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Pagination

List endpoints support pagination with the following query parameters:

- `page` - Page number (default: 1)
- `page_size` - Number of results per page (default: 30, max: 100)

**Example:**

```bash
GET /api/{version}/library/track/?page=1&page_size=50
```

**Response:**

```json
{
  "count": 150,
  "next": "/api/{version}/library/track/?page=2&page_size=50",
  "previous": null,
  "results": [...]
}
```

### Error Handling

Errors are returned in a consistent format:

```json
{
  "code": 2001,
  "message": "Validation failed",
  "details": {
    "field_name": {
      "message": "Field-specific error message",
      "code": "error_code",
      "details": {
        "value": "invalid_value",
        "requirement": "validation_requirement"
      }
    }
  }
}
```

Error codes are organized by category:
- `1000-1999`: Authentication/Authorization errors
- `2000-2999`: Validation errors
- `3000-3999`: Resource errors
- `4000-4999`: Business logic errors
- `5000-5999`: External service errors
- `9000-9999`: System/Internal errors

### Example: Uploading a Track

```bash
POST /api/{version}/library/track/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

file: @track.mp3
title: "Song Title"
artists_names[]: "Artist 1"
artists_names[]: "Artist 2"
genre: {genre_uuid}
```

The API will automatically:
1. Extract audio metadata from the file
2. Generate an audio fingerprint
3. Look up the track in MusicBrainz via AcoustID
4. Retrieve and store metadata (title, artist, album, etc.)
5. Associate the track with the authenticated user

## API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/token/` | POST | Obtain JWT access and refresh tokens |
| `/auth/token/refresh/` | POST | Refresh an access token |
| `/auth/spotify/` | GET | Initiate Spotify OAuth authentication |

### Users

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/users/` | GET, POST | List or create users |
| `/users/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a user |
| `/users/spotify/` | GET, POST | List or create Spotify users |

### Library - Tracks

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/library/track/` | GET, POST | List or upload tracks |
| `/library/track/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a track |
| `/library/spotify/` | GET, POST | List or sync Spotify library tracks |
| `/all-tracks/` | GET | List all tracks (user's library + Spotify) |

### Artists

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/artists/` | GET, POST | List or create artists |
| `/artists/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete an artist |
| `/spotify-artists/` | GET, POST | List or create Spotify artists |

### Albums

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/albums/` | GET, POST | List or create albums |
| `/albums/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete an album |

### Genres & Tags

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/genres/` | GET, POST | List or create genres |
| `/genres/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a genre |
| `/tags/` | GET, POST | List or create tags |
| `/tags/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a tag |

### Playlists

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/playlists/` | GET, POST | List or create playlists |
| `/playlists/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a playlist |
| `/manual-playlists/` | GET, POST | List or create manual playlists |
| `/genre-playlists/` | GET, POST | List or create genre-based playlists |
| `/tag-playlists/` | GET, POST | List or create tag-based playlists |

### Plays

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/plays/` | GET, POST | List or record play events |
| `/plays/{uuid}/` | GET, PUT, PATCH, DELETE | Retrieve, update, or delete a play event |

### Search

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/search/` | GET | Multi-model search across tracks, artists, albums, genres, and tags |

### API Documentation

Interactive API documentation is available at:

- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/schema/redoc/`
- **OpenAPI Schema**: `/api/schema/`

These endpoints provide comprehensive documentation of all available endpoints, request/response formats, and authentication requirements.

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

