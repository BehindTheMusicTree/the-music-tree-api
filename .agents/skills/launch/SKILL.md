---
name: launch
description: Use this skill when asked to run, start, dev-serve, or preview the-music-tree-api, or to confirm a change works in the real app. Covers required env setup (strict fail-fast env vars, no fallbacks) and the companion PostgreSQL + Audio Fingerprinter (AFP) Docker containers this API depends on.
---

# Launching the-music-tree-api locally

Django REST Framework API (Python 3.14) backing `grow-the-music-tree-frontend`.
Requires a PostgreSQL database (Docker) and, for audio-fingerprinting features,
a companion Audio Fingerprinter (AFP) service. Env var validation is strict —
required vars have no fallback and the app fails fast at startup if they're missing.

## 1. Prerequisites

- Python 3.14
- Docker + Docker Compose running (for the PostgreSQL container)
- System tools: `flac`, `ffmpeg`, `libchromaprint-tools`, `jq`, `postgresql-client`
  - Linux: `sudo bash scripts/install-dependencies.sh`
  - macOS: install the equivalents via Homebrew (script is Linux-oriented)

## 2. Environment file

Copy the dev template to the real env file and fill in the values:

```bash
test -e env/.env || cp env/dev/.env.dev_template env/.env
```

Note: CONTRIBUTING.md refers to this file as `env/dev/.env.dev.template`, but the
actual filename in this repo is `env/dev/.env.dev_template` (underscore, no second dot).

Required vars enforced with no fallback by `api/settings.py` (`load_required_secret_env_var`)
— missing any of these raises immediately on startup:

- `DB_BODZIFY_API_USER_PASSWORD`
- `ACOUSTID_API_KEY`
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `DJANGO_SECRET_KEY` (not present in the template — generate one, see below)

Other vars used for local Docker DB / filesystem setup are already in the template
(`DB_PORT=5433`, `DB_CONTAINER_NAME`, `DB_BODZIFY_API_DB_NAME`, `DB_BODZIFY_API_USERNAME`,
`DB_SUPERUSER_NAME`/`DB_SUPERUSER_PASSWORD`, `APP_IS_EXPOSED`, `DEBUG`, etc.).

Generate a Django secret key privately and write it directly to `env/.env` as
`DJANGO_SECRET_KEY` without printing it or exposing it in tool output. Do not
overwrite an existing key. The supplied `scripts/generate-django-secret-key.py`
prints its result, so do not run it in an agent session.

`AFP_*` vars (`AFP_CONTAINER_NAME`, `AFP_PORT`, `AFP_POST_ENDPOINT`) are only needed if
you're exercising audio fingerprinting/upload flows against the AFP container — they are
not read by `api/settings.py`, so the server boots without them.

## 3. Python environment (first run)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Filesystem and PostgreSQL

Use an existing local PostgreSQL instance configured for this project. Inspect
`env/.env` and the filesystem requirements in `scripts/setup-filesystem.sh`
before setting up paths: that script removes existing static-file contents.
The `scripts/run-db-container.sh` script removes the named container, may stop
and remove other containers using the configured port, and prunes Docker images.
Do not run either script without explicit authorization for those effects. Never
remove unrelated containers or data as part of launching the service.

Audio Fingerprinter can run separately from its own repository:
https://github.com/BehindTheMusicTree/audio-fingerprinter

## 5. Initialize a new local database (first run only)

Before running the following command, verify that the configured database is
local and explicitly new or empty, and that its role is dedicated to this
project. The script changes role privileges and loads fixtures that can replace
existing records. If the database is not known to be empty, do not run it or
load its fixtures; ask the user how to proceed.

```bash
bash scripts/init-django-data.sh
```

This creates the DB role/database (`scripts/init-db-and-role.sh`), runs
`makemigrations` + `migrate`, and loads fixtures from `api/fixtures/*.json`
(starting with `app.json`).

The reinitialization script can wipe data; do not run it without an explicit request.

## 6. Run the dev server

```bash
source .venv/bin/activate
python manage.py runserver
```

(Also configured in `.vscode/launch.json` as the "Python: Django" debug config.)
Defaults to `http://127.0.0.1:8000`. This is Django's local dev server — the
Gunicorn/`scripts/entrypoint.sh` path is only used inside the built Docker image.

## 7. Verify it's running

- `GET http://127.0.0.1:8000/api/docs/` — Swagger UI
- `GET http://127.0.0.1:8000/api/schema/redoc/` — ReDoc
- `GET http://127.0.0.1:8000/api/schema/` — raw OpenAPI schema
- `pytest` — run the test suite (see `testing.md` for scoped runs, e.g. `pytest api/test/view/track/`)

## Companion services summary

- **PostgreSQL** (required to boot): a local instance configured for this project.
- **Audio Fingerprinter / AFP** (only for fingerprinting/upload flows): separate repo
  `audio-fingerprinter`, run independently — not started by any script
  currently in this repo.
- **grow-the-music-tree-frontend**: the frontend consumer of this API; not required to
  run this API itself, but is the app that calls it.
