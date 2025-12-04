## Description

This PR consolidates workspace and dev-environment maintenance changes to improve reproducibility for contributors and cleanup local machine-specific configuration.

- Switches workspace-specific VS Code Python interpreter from a local absolute path to a workspace-relative interpreter.
- Adds README documentation for creating and using a `.venv` in the repository.
- Housekeeping: minor `CHANGELOG.md` update and test filename update, and a regenerated `0001_initial.py` header/imports refresh.

## Related Issue

N/A

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [x] 📚 Documentation update
- [x] ♻️ Refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [x] ✅ Test addition/update
- [x] 🔧 Configuration change
- [x] 🎨 Style/formatting changes
- [x] 🧹 Chore/maintenance

## Target Branch

- [x] `develop` (for features, bug fixes, chores, dependency updates from Dependabot)
- [ ] `main` (for hotfixes only)

## Changes Made

- `.vscode/settings.json`:
  - Replaced `python.pythonPath` with `python.defaultInterpreterPath` and set it to `${workspaceFolder}/.venv/bin/python`.
- `README.md`:
  - Added a "Developer environment (recommended)" section showing how to create and activate `.venv`, install dependencies and how to use the VS Code interpreter selection feature.
- `CHANGELOG.md` and `UploadedTrackTestFilename.py`:
  - Minor maintenance edits (housekeeping, see commit history).
- `bodzify_api/migrations/0001_initial.py`:
  - Updated timestamp/imports due to local evolution of models and utility code.

## Testing

- [x] All existing tests pass locally
- [ ] New tests added (if applicable)
- [x] Manual testing completed (if applicable)

**Test commands:**

```bash
# create and activate .venv and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# run tests
pytest
```

- Manual check: VS Code picked `.venv` automatically or select via `Python: Select Interpreter`.
- Confirm that `python.pythonPath` is no longer committed and `python.defaultInterpreterPath` points to `${workspaceFolder}/.venv/bin/python`.

## Checklist

### Code Quality
- [x] Code follows project style guidelines ([code-style.md](code-style.md))
- [x] Code follows Django best practices
- [ ] Type hints added where appropriate
- [x] No debug statements or commented-out code
- [x] One class per file (if applicable)
- [ ] Field name constants used (if applicable)

### Tests
- [x] All tests pass: `pytest`
- [ ] New features have corresponding tests
- [ ] Bug fixes include regression tests
- [x] Tests follow naming convention: `test_{scenario}_then_{expected_result}`
- [x] Each test focuses on a single scenario

### Documentation
- [x] Docstrings updated (only when needed)
- [x] README updated (if applicable)
- [x] CHANGELOG.md updated in `[Unreleased]` section
- [ ] Type hints added/updated

### Git Hygiene
- [x] Commit messages follow convention: `<type>(<scope>): <summary>`
- [x] Branch is up to date with target branch
- [x] Branch follows naming convention (`feature/`, `chore/`, `dependabot/`, `hotfix/`, `release/`)
- [x] No accidental commits (large files, secrets, personal configs)

## Breaking Changes

- [ ] This PR includes breaking changes
- [ ] Breaking changes are documented in the description above
- [ ] Migration path provided (if applicable)

**Breaking Changes:**

N/A

## Screenshots (if applicable)

N/A

## Additional Notes

- The PR template recommends working with `.github/pr-descriptions/` (git-ignored) for draft PR descriptions to avoid committing private or partial drafts. If you prefer, keep your local draft in that directory and copy its contents into the PR when creating it.
- The repository uses `python.defaultInterpreterPath` which is the modern interpreter setting used by the Python extension; `python.pythonPath` is deprecated.

## Reviewer Notes

- Please confirm the `.vscode` workspace settings and `README` changes are correct and sufficient to streamline onboarding.
- Check the migration head to ensure only timestamp/import imports were updated; if any schema changes got included accidentally, flag them for separation into a distinct PR.

---

If you prefer, I can extract the venv-specific portion into a smaller, focused PR and keep migrations and test changes in a separate PR—just say which approach you'd like.