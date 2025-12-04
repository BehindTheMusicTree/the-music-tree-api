# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Changelog Best Practices

### General Principles

- Changelogs are for humans, not machines.
- Include an entry for every version, with the latest first.
- Group similar changes under: Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI.
- **"Test" is NOT a valid changelog category** - tests should be mentioned within the related feature or fix entry, not as standalone entries.
- Use an "Unreleased" section for upcoming changes.
- Follow Semantic Versioning where possible.
- Use ISO 8601 date format: YYYY-MM-DD.
- Avoid dumping raw git logs; summarize notable changes clearly.

### Guidelines for Contributors

All contributors (including maintainers) should update `CHANGELOG.md` when creating PRs:

1. **Add entries to the `[Unreleased]` section** - Add your changes under the appropriate category (Added, Changed, Improved, Deprecated, Removed, Fixed, Documentation, Performance, CI)
2. **Follow the changelog format** - See examples below and `.cursor/rules/changelog-best-practices.mdc` for detailed guidelines
3. **Group related changes** - Similar changes should be grouped together
4. **Be descriptive** - Write clear, user-focused descriptions of what changed
5. **Mention tests when relevant** - Tests should be mentioned within the related feature or fix entry, not as standalone entries

**Example:**

```markdown
## [Unreleased]

### Added

- **Track API**: Added batch upload endpoint for multiple tracks
  - Includes comprehensive unit tests covering various file formats and error scenarios
  - Supports parallel upload processing for improved performance

- **Genre Hierarchy**: Added support for custom genre tree import via JSON
  - Includes validation tests for tree structure and circular reference detection

### Fixed

- **Track Upload**: Fixed issue with handling large audio files exceeding size limits
  - Includes regression tests to prevent future occurrences
  - Improved error messages for better user feedback

### CI

- **Branch Protection**: Added automated enforcement of Git Flow branching rules
  - Blocks invalid PRs to main and develop branches
```

**Note:** During releases, maintainers will move entries from `[Unreleased]` to a versioned section (e.g., `## [0.2.8] - 2025-01-XX`).

## [Unreleased]

### Added

- **Git Worktree Scripts**: Added npm `git-worktree-scripts` package (v1.4.0) for managing git worktrees
  - Includes `setup-worktree.sh` script for automated worktree setup with virtual environment and dependencies
  - Added `.git-worktree-copy` configuration for copying gitignored files to new worktrees
    - Copies `env/.venv` Python virtual environment
    - Copies fixture files from `bodzify_api/fixtures/*.json`
  - Integrated filesystem setup into `setup-worktree.sh` for automatic directory and log file creation

### CI

- **GitHub Automation**:
  - Auto-labeler workflow (`.github/workflows/labeler.yml`) for automatic PR labeling based on file paths
  - Branch protection workflow (`.github/workflows/branch-protection.yml`) to enforce Git Flow rules
    - Blocks PRs to `main` from non-hotfix/release branches
    - Blocks PRs to `develop` from invalid branch types
  - Issue templates for bug reports and feature requests
  - Pull request template with comprehensive checklist
  - GitHub Discussions setup with category templates

- **Branch Protection**: Added automated enforcement of Git Flow branching rules
  - PRs to `main` must come from `hotfix/*` or `release/*` branches only
  - PRs to `develop` must come from `feature/*`, `chore/*`, `hotfix/*`, or `release/*` branches only
  - Provides clear error messages when branch rules are violated

- **CI/CD**: Updated GitHub Actions workflow to use `develop` branch instead of `dev`
  - Updated Python version to 3.14 in CI workflows
  - Added branch protection checks for Git Flow enforcement

### Changed

- **Audio Metadata**: Replaced audio metadata management module with `audiometa-python` (bumped to `0.8.1` in `requirements.txt`)
- **Dependencies**: 
  - Updated `Django` from 5.0.3 to 5.2.8
  - Updated `asgiref` from 3.7.2 to 3.8.1 for Django 5.2.8 compatibility
  - Updated `django-stubs` from 5.1.1 to 5.2.1 for Django 5.2.8 compatibility
  - Updated `django-filter` from 22.1 to 25.2 for Python 3.14 compatibility (fixes `pkgutil.find_loader` removal)
  - Updated `django-polymorphic` from 3.1.0 to 4.1.0 to resolve pkg_resources deprecation warning and ensure Django 5.2 compatibility
  - **Audio Metadata**: Replace audio metadata management module with audiometa-python 0.8.0
  - Removed `mutagen` from direct dependencies. No longer needed as direct dependency since all audio operations now use `audiometa-python`

### Fixed

- **Filesystem Setup**: Fixed `setup-filesystem.sh` to check for `DJANGO_LOG_DIR` instead of `DJANGO_LOGS_DIR` to properly create log directories
- **Filter Backend**: Added `get_schema_operation_parameters` method to `ConsistentParametersFilterBackend` for drf-spectacular compatibility with django-filter 25.2
- **Django 6.0 Compatibility**: Replaced deprecated `CheckConstraint.check` with `condition` parameter in all model constraints
  - Updated 6 model files: `CriteriaType`, `Criteria`, `Artist`, `Album`, `FingerprintMissingCauseCode`, `ManualPlaylist`
  - Updated migration file `0001_initial.py` to use new syntax
  - Resolves Django 6.0 deprecation warnings for `CheckConstraint.check`

### Documentation

- **Project Management**: Added `TODO.md` for tracking future work and improvements
  - Categorized by priority (high, medium, low)
  - Organized by features, testing, and infrastructure

- **Contributing Documentation**: Comprehensive contributing guide with strict Git Flow workflow
  - Detailed branch naming and merging rules for `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`, and `chore/*` branches
  - Installation and setup instructions
  - Code style guidelines and development best practices
  - Pre-PR checklist and review process
  - Release process documentation

- **Development Guidelines**: Added `DEVELOPMENT.md` with comprehensive coding standards
  - Code quality practices and conventions
  - Django best practices for models, serializers, views, and filtering
  - Type checking and error handling guidelines
  - Documentation standards

- **Cursor Rules**: Added AI assistant rules to enforce project standards
  - Git Flow workflow enforcement
  - Commit message convention (Conventional Commits)
  - Pull request title convention
  - Issue template usage guidelines
  - Pre-PR checklist enforcement
  - Issue descriptions in separate version-controlled files
  - PR descriptions in git-ignored directory for local drafting
  - Test naming convention and structure guidelines
  - Changelog best practices

- **README**: Simplified `README.md` to provide high-level overview with links to detailed documentation
  - Moved detailed setup instructions to `CONTRIBUTING.md`
  - Added badges for license, Python version, and Django version

- **Contributing Guide**: Reorganized installation steps in `CONTRIBUTING.md` for logical flow
  - Environment variables setup before scripts that use them
  - Improved step-by-step instructions clarity

- **License**: Added Apache License 2.0

- **Code of Conduct**: Added Contributor Covenant 2.1

### CI

<<<<<<< HEAD
- **Branch Protection**: Added automated enforcement of Git Flow branching rules
  - PRs to `main` must come from `hotfix/*` or `release/*` branches only
  - PRs to `develop` must come from `feature/*`, `chore/*`, or `dependabot/*` branches only
  - Provides clear error messages when branch rules are violated

- **CI/CD**: Updated GitHub Actions workflow to use `develop` branch instead of `dev`
  - Updated Python version to 3.14 in CI workflows
  - Added branch protection checks for Git Flow enforcement

- **GitHub Automation**:
  - Auto-labeler workflow (`.github/workflows/labeler.yml`) for automatic PR labeling based on file paths
  - Branch protection workflow (`.github/workflows/branch-protection.yml`) to enforce Git Flow rules
    - Blocks PRs to `main` from non-hotfix/release branches
    - Blocks PRs to `develop` from invalid branch types
  - Issue templates for bug reports and feature requests
  - Pull request template with comprehensive checklist
  - GitHub Discussions setup with category templates

=======
>>>>>>> origin/develop
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
- Enable delete criteria

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