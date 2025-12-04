## Description

This PR represents a broad infrastructure and audio metadata refactor that includes dependency upgrades, model/migration updates, audio metadata processing refactor, CI/workflow improvements, and developer UX improvements (workspace venv, README updates).

Major categories included:

- Audio metadata refactor: move to `audiometa-python` and update internal adapter/implementations under `bodzify_api/utils/audio_file_metadata`.
- Django and dependency upgrades: updated to `Django==5.2.8` and other package bumps for Python 3.14 compatibility.
- Model & migration updates: updated CheckConstraint usage, model rearrangements; refreshed `0001_initial.py` migration header, imports and constraints.
- Tests: updated and added tests across many modules to accommodate the refactor and dependency updates.
- CI and GitHub workflow updates and branch protection rules.
- Developer experience updates: workspace `.venv` usage in VS Code settings and README contribution/setup instructions.
- Scripts and utilities: several scripts updated (worktree, setup, CI-utils) and file paths adjusted.

## Related Issue

N/A

## Type of Change

- [x] 🐛 Bug fix (non-breaking change which fixes an issue)
- [x] ✨ New feature (non-breaking change which adds functionality)
- [x] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] 📚 Documentation update
- [x] ♻️ Refactoring (no functional changes)
- [x] ⚡ Performance improvement
- [x] ✅ Test addition/update
- [x] 🔧 Configuration change
- [x] 🎨 Style/formatting changes
- [x] 🧹 Chore/maintenance

## Target Branch

- [x] `develop` (for features, bug fixes, chores, dependency updates)
- [ ] `main` (for hotfixes only)

## Changes Made (high level)

- Replaced the custom `audiometa` logic with `audiometa-python` and refactored `bodzify_api/utils/audio_file_metadata/` as the new home for audio metadata handling (includes exceptions, adapters, utility types).
- Moved some helper modules and changed import paths to `bodzify_api/utils/audio_file_metadata` and removed legacy `audiometa_adapter` files when refactored.
- Upgraded `Django` and several libraries in `requirements.txt` to ensure Python 3.14 compatibility and fix deprecation warnings (Django 5.2.8, django-filter 25.2, django-stubs 5.2.1, django-polymorphic 4.1.0, etc.).
- Updated models to adopt the newer `CheckConstraint(condition=...)` syntax and changed related code & migrations to reflect the latest API.
- Regenerated and updated `bodzify_api/migrations/0001_initial.py` to reflect model & import changes.
- Tests updated across the project to handle library changes and behavior changes introduced by the refactor (audio metadata, fingerprinting, file metadata, etc.).
- CI and GitHub workflows updated to modernized pipelines across `ci.yaml`, `build.yml`, `test.yml`, `publish.yml` and more; updated branch protection rules and added auto-labeling workflows.
- Developer setup changed to recommend and use a `.venv` workspace virtualenv; `.vscode/settings.json` now references `${workspaceFolder}/.venv/bin/python`.
- README and CONTRIBUTING documentation updated including `DEVELOPMENT.md` with developer onboarding steps.
- Script updates: new or updated scripts live under `scripts/` for worktree and other automation tasks.
- Minor housekeeping: `CHANGELOG.md` updated with Unreleased entries and organizational changes, logs cleaned up.

## Notable Files Changed

(This is a succinct list; see branch diff for full detail)

- `bodzify_api/utils/audio_file_metadata/*`
- `bodzify_api/utils/audiometa_adapter*` (moved/renamed/replaced)
- `requirements.txt` — dependency upgrades
- `bodzify_api/migrations/0001_initial.py`
- `bodzify_api/model/*` (CriteriaType, Criteria, Artist, Album, ManualPlaylist, etc.)
- `bodzify_api/test/*` — Ranged updates across tests to accommodate new behavior
- `.github/workflows/*` — CI pipeline updates
- `.vscode/settings.json` — workspace-relative python interpreter change
- `README.md`, `CONTRIBUTING.md`, `DEVELOPMENT.md`, `CHANGELOG.md` — docs
- `scripts/*` — several script updates

## Migration Impact

- Migrations were regenerated/updated to reflect model changes. If you are migrating an existing database against this branch, make sure to test migration flows on a staging DB.

**Recommended migration verification:**
```bash
python manage.py makemigrations --check
python manage.py migrate --plan
```

## Tests and verification

- Run the complete test suite locally after creating `.venv` and installing dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

- Manual checks:
  - Verify `bodzify_api` audio metadata pipelines (fingerprint + metadata extraction) behave as expected.
  - Check VS Code picks up `.venv` correctly or use `Python: Select Interpreter`.
  - CI checks should run on PR creation: `test.yml`, `build.yml`, and `publish.yml`.

## Breaking Changes

This branch includes several migration and model changes; expect potential breaking changes for projects running prior migrations.

- Schema changes may have been introduced if model definitions were updated beyond constraint syntax.
- If a rework of the audio metadata logic changes behavior, validate against real files for regression.

## Reviewer Notes

- Focus on the `audio_file_metadata` module and ensure the adapter/separation is correct.
- Validate all model migrations are intentionally required and no accidental schema modifications occurred.
- Verify `requirements.txt` upgrades are compatible with production. Some versions are upgraded to Python 3.14 compatible versions.

---

If you prefer a more narrowly-focused PR, I can split this into multiple PRs (e.g., infra vs audio vs docs).