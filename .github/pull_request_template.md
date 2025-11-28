## Description

<!-- Provide a clear and concise description of what this PR does -->
<!-- Note: PR descriptions should be drafted in `.github/pr-descriptions/` directory (git-ignored) before creating the PR -->

## Related Issue

<!-- Link to related issue(s). Use "Fixes #123" or "Closes #123" to auto-close issues -->
<!-- Example: Fixes #123 -->

## Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] ♻️ Refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test addition/update
- [ ] 🔧 Configuration change
- [ ] 🎨 Style/formatting changes
- [ ] 🧹 Chore/maintenance

## Target Branch

<!-- Mark the target branch with an "x" -->

- [ ] `develop` (for features, bug fixes, chores)
- [ ] `main` (for hotfixes only)

## Changes Made

<!-- Describe the changes in detail -->

## Testing

<!-- Describe the tests you ran and how to verify your changes -->

- [ ] All existing tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing completed (if applicable)

**Test commands:**
```bash
# Add test commands here
pytest
```

## Checklist

<!-- Mark completed items with an "x" -->

### Code Quality
- [ ] Code follows project style guidelines ([code-style.md](code-style.md))
- [ ] Code follows Django best practices
- [ ] Type hints added where appropriate
- [ ] No debug statements or commented-out code
- [ ] One class per file (if applicable)
- [ ] Field name constants used (if applicable)

### Tests
- [ ] All tests pass: `pytest`
- [ ] New features have corresponding tests
- [ ] Bug fixes include regression tests
- [ ] Tests follow naming convention: `test_{scenario}_then_{expected_result}`
- [ ] Each test focuses on a single scenario

### Documentation
- [ ] Docstrings updated (only when needed)
- [ ] README updated (if applicable)
- [ ] CHANGELOG.md updated in `[Unreleased]` section
- [ ] Type hints added/updated

### Git Hygiene
- [ ] Commit messages follow convention: `<type>(<scope>): <summary>`
- [ ] Branch is up to date with target branch
- [ ] Branch follows naming convention (`feature/`, `chore/`, `hotfix/`, `release/`)
- [ ] No accidental commits (large files, secrets, personal configs)

## Breaking Changes

<!-- If this PR includes breaking changes, document them here -->

- [ ] This PR includes breaking changes
- [ ] Breaking changes are documented in the description above
- [ ] Migration path provided (if applicable)

**Breaking Changes:**
<!-- List breaking changes here -->

## Screenshots (if applicable)

<!-- Add screenshots or GIFs to help explain your changes -->

## Additional Notes

<!-- Any additional information, context, or notes for reviewers -->

## Reviewer Notes

<!-- Optional: Add any specific areas you'd like reviewers to focus on -->

