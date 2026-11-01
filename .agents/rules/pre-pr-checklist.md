# Pre-PR Checklist

Before submitting a Pull Request, ensure all checks are completed. This checklist helps maintain code quality and consistency.

## Code Quality

- ✅ Follow code style standards in `code-style.md`
- ✅ Code follows Django best practices
- ✅ Type hints are used where appropriate
- ✅ No debug statements or commented-out code
- ✅ One class per file (see `one-class-per-file.md`)
- ✅ Use field name constants from `Fields.py` files (see `field-name-constants.md`)
- ✅ Private resource filtering includes user in query (see `private-resource-filtering.md`)

## Tests

- ✅ All tests pass: `pytest`
- ✅ New features have corresponding tests
- ✅ Bug fixes include regression tests
- ✅ Tests follow naming convention: `test_{scenario}_then_{expected_result}` (see `test-naming-convention.md`)
- ✅ Each test focuses on a single scenario (see `divide-test-cases.md`)
- ✅ Use `assert` instead of `assertEqual` (see `use-assert-not-assertequal.md`)

## Documentation

- ✅ Update docstrings for new functions/classes (only when needed - see `no-useless-comments.md`)
- ✅ Update README or other documentation if adding new features or changing behavior
- ✅ Add/update type hints where appropriate
- ✅ Update `CHANGELOG.md` with changes in the `[Unreleased]` section

## Git Hygiene

- ✅ Commit messages follow the commit message convention (see `commit-message-convention.md`)
- ✅ Branch is up to date with target branch (`develop` for features, `main` for hotfixes)
- ✅ Branch follows naming convention (`feature/`, `chore/`, `hotfix/`, `release/`)
- ✅ No accidental commits (large files, secrets, personal configs)

## Branch Target

- ✅ Feature branches target `develop` branch
- ✅ Hotfix branches target `main` branch
- ✅ Release branches target both `main` and `develop` (maintainers only)

## Quick Pre-PR Command

```bash
# Run all checks at once
pytest && git status
```
