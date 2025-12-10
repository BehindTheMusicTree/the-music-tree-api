# TheMusicTreeAPI

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)

> 🔨 **Work in Progress** - Will be published open source soon! 🚀

TheMusicTreeAPI is the API companion to [GrowTheMusicTree](https://github.com/BehindTheMusicTree/grow-the-music-tree), giving developers, researchers, and music platforms access to the full genre hierarchy, detailed metadata, and intelligent genre detection. Built with Django REST Framework and PostgreSQL, it enables personalized user profiling based on listening habits, delivers accurate track and artist classifications, and provides data-driven recommendations.

Perfect for powering music discovery, streaming personalization, event recommendations, and listener analytics, TheMusicTreeAPI brings the intelligence of the genre tree to any app or service.

For more information about the project's vision, goals, and technical approach, see [VISION.md](VISION.md).

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

## Ecosystem

TheMusicTreeAPI is part of the [BehindTheMusicTree](https://github.com/behindthemusictree) ecosystem, which centers around:

- **[GrowTheMusicTree](https://github.com/BehindTheMusicTree/grow-the-music-tree)**: The definitive, interactive map of global music genres—a tree-shaped framework that organizes genres, subgenres, and microgenres. Built through crowd-sourced curation and expert input, it serves as the ultimate reference for understanding music genres.
- **TheMusicTreeAPI**: This REST API that provides programmatic access to the genre hierarchy and intelligence, enabling developers to integrate genre classification and recommendations into their platforms.

## Usage
TODO

## API Endpoints
TODO

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

