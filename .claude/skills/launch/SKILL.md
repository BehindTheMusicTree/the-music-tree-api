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
cp env/dev/.env.dev_template env/.env
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

Generate a Django secret key and add it to `env/.env` as `DJANGO_SECRET_KEY`:

```bash
python scripts/generate-django-secret-key.py
```

`AFP_*` vars (`AFP_CONTAINER_NAME`, `AFP_PORT`, `AFP_POST_ENDPOINT`) are only needed if
you're exercising audio fingerprinting/upload flows against the AFP container — they are
not read by `api/settings.py`, so the server boots without them.

## 3. Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Filesystem setup

```bash
bash scripts/setup-filesystem.sh
```

Creates the static files, Django/Gunicorn log, media/library, and tmp-upload
directories referenced by the env vars.

## 5. Start the companion PostgreSQL container

```bash
bash scripts/run-db-container.sh
```

Pulls and runs the Postgres container defined by `DB_IMAGE_REPO`/`DB_VERSION`,
publishing it on `DB_PORT` (`5433` in the template, mapped to Postgres' `5432`
inside the container). Requires Docker to be running.

Note: CONTRIBUTING.md and DEVELOPMENT.md reference a `scripts/run-db-and-afp-containers.sh`
that also starts the Audio Fingerprinter (AFP) container — that script does not currently
exist in `scripts/`; only `scripts/run-db-container.sh` (DB only) is present. If you need
the AFP companion service, run it separately from its own repo:
https://github.com/BehindTheMusicTree/bodzify-audio-fingerprinter-flask

## 6. Initialize the database (first run)

```bash
bash scripts/init-django-data.sh
```

This creates the DB role/database (`scripts/init-db-and-role.sh`), runs
`makemigrations` + `migrate`, and loads fixtures from `api/fixtures/*.json`
(starting with `app.json`).

To wipe and redo this (destructive — prompts for confirmation, `-s` skips the prompt):

```bash
bash scripts/reinit-django-data-USE-WITH-CAUTION.sh
```

## 7. Run the dev server

```bash
python manage.py runserver
```

(Also configured in `.vscode/launch.json` as the "Python: Django" debug config.)
Defaults to `http://127.0.0.1:8000`. This is Django's local dev server — the
Gunicorn/`scripts/entrypoint.sh` path is only used inside the built Docker image.

## 8. Verify it's running

- `GET http://127.0.0.1:8000/api/docs/` — Swagger UI
- `GET http://127.0.0.1:8000/api/schema/redoc/` — ReDoc
- `GET http://127.0.0.1:8000/api/schema/` — raw OpenAPI schema
- `pytest` — run the test suite (see `testing.md` for scoped runs, e.g. `pytest api/test/view/track/`)

## Companion services summary

- **PostgreSQL** (required to boot): Docker container via `scripts/run-db-container.sh`.
- **Audio Fingerprinter / AFP** (only for fingerprinting/upload flows): separate repo
  `bodzify-audio-fingerprinter-flask`, run independently — not started by any script
  currently in this repo.
- **grow-the-music-tree-frontend**: the frontend consumer of this API; not required to
  run this API itself, but is the app that calls it.
