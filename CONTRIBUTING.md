# 🧭 Contributing Guidelines

Thank you for your interest in contributing!

This project is currently maintained by a solo developer, but contributions, suggestions, and improvements are welcome.

## Table of Contents

- [🧑‍🤝‍🧑 Contributors vs Maintainers](#-contributors-vs-maintainers)
  - [Roles Overview](#roles-overview)
  - [Infrastructure & Automation Permissions](#infrastructure--automation-permissions)
- [🧱 Development Workflow](#-development-workflow)
  - [0. Fork & Clone](#0-fork--clone)
  - [1. Environment Setup](#1-environment-setup)
  - [2. Branching](#2-branching)
  - [3. Developing](#3-developing)
  - [4. Testing](#4-testing)
  - [5. Committing](#5-committing)
  - [6. Pull Request Process](#6-pull-request-process)
    - [6.1. Pre-PR Checklist](#61-pre-pr-checklist)
    - [6.2. Opening a Pull Request](#62-opening-a-pull-request)
  - [7. Releasing _(For Maintainers)_](#7-releasing-for-maintainers)
- [🪪 License & Attribution](#-license--attribution)
- [📜 Code of Conduct](#-code-of-conduct)
- [🌍 Contact & Discussions](#-contact--discussions)

## Contributors vs Maintainers

### Roles Overview

**Contributors**

Anyone can be a contributor by:

- Submitting bug reports or feature requests via GitHub Issues (use the issue templates: [Bug Report](.github/ISSUE_TEMPLATE/bug_report.yml) and [Feature Request](.github/ISSUE_TEMPLATE/feature_request.yml))
- Proposing code changes through Pull Requests (the PR template will guide you through the process)
- Improving documentation
- Participating in discussions
- Testing and providing feedback

**Maintainers**

The maintainer(s) are responsible for:

- Reviewing and merging Pull Requests
- Managing releases and versioning
- Ensuring code quality and project direction
- Responding to critical issues
- Maintaining the project's infrastructure
- Creating and managing hotfix branches for urgent production fixes
- Creating and managing release branches for preparing releases
- Moving "Unreleased" changelog entries to versioned sections during releases
- Managing repository automation (stale issues/PRs, auto-labeling, auto-assignment, etc.)

**Important:** Even maintainers must go through Pull Requests. No direct commits to `main` or `develop` are allowed - all changes, including those from maintainers, must be submitted via Pull Requests and go through the standard review process.

_Note: Contributors can submit fixes for critical issues via feature branches. Maintainers may promote these to hotfix branches when urgent production fixes are needed._

### Infrastructure & Automation Permissions

**Repository automation policies (maintainer-only):**

- Publishing workflows (`.github/workflows/*.yml`) - handles sensitive secrets and can publish Docker images
- Stale issues/PRs workflow - affects repository management policies
- Auto-assignment workflows - affects review process
- Auto-labeler workflow (`.github/workflows/labeler.yml`) - automatically labels PRs based on changed files
- Other automation workflows that affect repository management

**Auto-labeling configuration (contributors can suggest changes via PRs):**

- Auto-labeling configuration (`.github/labeler.yml`) - contributors can suggest updates when adding new features/components
- Example: If adding a new API endpoint, contributor can suggest adding label rules for that component
- Maintainers review and approve label configuration changes

**Why most automation is maintainer-only:**

- These workflows implement repository policies and management decisions
- Changes can affect how issues/PRs are handled, categorized, and maintained
- They require understanding of project management strategy

**What contributors can do:**

- Suggest changes to auto-labeling configuration (`.github/labeler.yml`) via PRs, especially when adding new features/components
- Suggest improvements or report issues with automation via GitHub Issues
- Add/remove labels on their own issues and PRs (type labels like `bug`, `enhancement`, priority labels, etc.)
- Discuss automation behavior in discussions or issues

**What contributors cannot do:**

- Modify automation workflows (stale, auto-assignment, etc.) - these are policy decisions
- Create or delete repository labels (maintainer-only) - repository labels are the label definitions (like `bug`, `enhancement`, `api`, `track`) that exist in the repository's label list
- Modify labels on issues/PRs they didn't create (unless they have write access)

Currently, this project has a solo maintainer, but the role may expand as the project grows.

## 🧱 Development Workflow

We follow a **strict Git Flow** model:

**Workflow steps:** Fork & Clone → Environment Setup → Branching → Developing → Testing → Committing → Pull Request Process (including Pre-PR Checklist) → Releasing _(For Maintainers)_

### 0. Fork & Clone

**For contributors:**

1. Fork the repository on GitHub
2. Clone your fork:

   ```bash
   git clone https://github.com/YOUR-USERNAME/bodzify-api-django.git
   cd bodzify-api-django
   ```

**For maintainers:**

Clone the main repository directly:

```bash
git clone https://github.com/mignot/bodzify-api-django.git
cd bodzify-api-django
```

### 1. Environment Setup

Ensure you're using:

- **Python 3.14**

- Virtual environment with dependencies:

  ```bash
  python -m venv .venv
  source .venv/bin/activate  # (Linux/macOS)
  .venv\Scripts\activate     # (Windows)
  pip install -r requirements.txt
  ```

- **PostgreSQL database** - The project requires PostgreSQL. You can use Docker Compose or a local PostgreSQL installation.

- **Environment variables** - Create a copy of `env/dev/.env.dev.template` as `env/.env` and set the required values. See [README.md](README.md) for details on required environment variables.

- **System dependencies** (required for testing and development):

  To ensure your local environment matches CI exactly, use the automated installation scripts:

  ```bash
  # Ubuntu/Linux
  ./scripts/install-dependencies.sh

  # macOS
  # Install dependencies via Homebrew or use the Linux script as reference
  ```

  **Required tools:**
  - PostgreSQL client libraries
  - Audio processing tools (if working with audio features)
  - Docker and Docker Compose (for running database and services)

### 2. Branching

We follow **strict Git Flow** with the following branch structure:

#### Main Branch (`main`)

- The production-ready, stable branch
- All tests must pass before merging
- Releases are tagged from `main`
- **No direct commits allowed** - All changes must go through Pull Requests, including changes from maintainers
- Only receives merges from `release/*` and `hotfix/*` branches

#### Develop Branch (`develop`)

- The integration branch for ongoing development
- All feature branches merge into `develop`
- `develop` is merged into `main` via release branches
- **No direct commits allowed** - All changes must go through Pull Requests

#### Feature Branches (`feature/<name>`)

- Create one for each new feature or bug fix
- Branch from `develop`
- Include issue numbers when applicable: `feature/123-add-ogg-support`
- Examples:

  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b feature/improve-genre-classification

  git checkout -b feature/123-add-ogg-support        # With issue number
  git checkout -b feature/456-fix-id3v1-encoding    # With issue number
  ```

- Merge into `develop` via Pull Request when complete and tested

#### Release Branches (`release/<version>`) _(For Maintainers)_

- Created from `develop` when preparing a new release
- Used for final testing, bug fixes, and version bumping
- Examples:

  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b release/v0.2.1
  ```

- Only bug fixes and release-related changes go into release branches
- When ready, merge into both `main` (for production) and `develop` (to keep develop up to date)
- Tag the release on `main` after merging

#### Hotfix Branches (`hotfix/<name>`) _(For Maintainers)_

- For urgent bug fixes on production versions
- Branch from `main`
- Include issue numbers when applicable: `hotfix/789-critical-bug`
- Examples:

  ```bash
  git checkout main
  git pull origin main
  git checkout -b hotfix/critical-metadata-bug

  git checkout -b hotfix/789-critical-security-patch   # With issue number
  ```

- Contributors can submit fixes via feature branches that maintainers may promote to hotfixes if needed
- When complete, merge into both `main` (for immediate production fix) and `develop` (to keep develop up to date)

#### Chore Branches (`chore/<name>`)

- For maintenance, infrastructure, and configuration work
- Branch from `develop`
- Include issue numbers when applicable: `chore/234-update-dependencies`
- Examples: repository setup, CI/CD changes, dependency updates, documentation infrastructure
- Examples:

  ```bash
  git checkout develop
  git pull origin develop
  git checkout -b chore/github-setup
  git checkout -b chore/update-dependencies
  git checkout -b chore/234-update-dependencies        # With issue number
  ```

- Merge into `develop` via Pull Request when complete

### 3. Developing

See [code-style.md](code-style.md) for coding standards and best practices. Key points:

- One class per file
- Use field name constants from `Fields.py` files
- Follow Django best practices
- Use type hints where appropriate
- Follow the project's code style conventions

### 4. Testing

We use pytest for all automated testing with Django.

#### Quick Reference

```bash
# Run all tests
pytest

# Run tests for a specific module
pytest bodzify_api/test/view/track/

# Run tests with coverage
pytest --cov=bodzify_api --cov-report=html --cov-report=term-missing

# Run tests with verbose output
pytest -v

# Run a specific test file
pytest bodzify_api/test/view/track/test_specific.py
```

**Test Structure:**

- Tests are located in `bodzify_api/test/`
- Follow the naming convention: `test_{scenario}_then_{expected_result}`
- Use `assert` instead of `assertEqual`
- Each test should focus on a single scenario

### 5. Committing

We follow a structured commit format inspired by [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).

**IMPORTANT:** Always activate the project's virtual environment (`.venv`) before committing if you're using pre-commit hooks.

**Quick reference:**

- Format: `<type>(<scope>): <summary>`
- Activate virtual environment: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)

**Commit Types:**

- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring
- `docs` - Documentation update
- `chore` - Maintenance / infrastructure
- `test` - Adding or updating tests
- `style` - Formatting / lint-only changes
- `ci` - CI/CD pipeline changes

**Examples:**

- `feat(track): add audio fingerprint support`
- `fix(genre): handle duplicate genre names`
- `docs: update API documentation`
- `test(track): add test for track upload`
- `chore: update dependencies`

**Commit Message Guidelines:**

- Use imperative mood ("Add…", "Fix…", "Update…")
- Keep summary under ~70 characters
- Include issue/ticket IDs when applicable (e.g., `fix(#482): handle null values`)
- Be descriptive but concise

### 6. Pull Request Process

#### 6.1. Pre-PR Checklist

Before submitting a Pull Request, ensure the following checks are completed:

**1. Code Quality**

- ✅ Follow code style standards in [code-style.md](code-style.md)
- ✅ Code follows Django best practices
- ✅ Type hints are used where appropriate
- ✅ No debug statements or commented-out code

**2. Tests**

- ✅ All tests pass: `pytest`
- ✅ New features have corresponding tests
- ✅ Bug fixes include regression tests
- ✅ Tests follow the naming convention: `test_{scenario}_then_{expected_result}`
- ✅ Each test focuses on a single scenario

**3. Documentation**

- ✅ Update docstrings for new functions/classes (only when needed)
- ✅ Update README or other documentation if adding new features or changing behavior
- ✅ Add/update type hints where appropriate
- ✅ Update `CHANGELOG.md` with your changes in the `[Unreleased]` section
- ⚠️ Update CONTRIBUTING.md only in exceptional cases

**4. Git Hygiene**

- ✅ Commit messages follow the commit message convention
- ✅ Branch is up to date with target branch (`develop` for features, `main` for hotfixes)
- ✅ No accidental commits (large files, secrets, personal configs)
- ✅ Branch follows naming convention (`feature/`, `chore/`, `hotfix/`, `release/`)

**5. Branch Target**

- ✅ Feature branches target `dev` branch
- ✅ Hotfix branches target `main` branch
- ✅ Release branches target both `main` and `dev` (maintainers only)
- ✅ Chore branches target `dev` branch

#### For Maintainers (Before Opening/Merging a PR)

**All Contributor Checks Plus:**

**1. Code Review**

- ✅ Code follows project conventions and style
- ✅ Logic is sound and well-structured
- ✅ Error handling is appropriate
- ✅ Performance considerations addressed (if applicable)
- ✅ Django best practices are followed

**2. Testing Verification**

- ✅ CI tests pass on all platforms and Python versions
- ✅ Test coverage is adequate
- ✅ Edge cases are handled
- ✅ Integration with existing features works correctly

**3. Documentation Review**

- ✅ API changes are documented
- ✅ Breaking changes are clearly marked and documented
- ✅ Examples and usage are updated if needed
- ✅ Update CONTRIBUTING.md if changing development workflow

**4. Compatibility Verification**

- ✅ Breaking changes have proper versioning plan (major version bump)
- ✅ Backward compatibility maintained (unless intentional breaking change)
- ✅ Migration path documented for breaking changes
- ✅ Dependencies are up to date and compatible

**5. Final Checks**

- ✅ PR description is clear and complete
- ✅ All review comments are addressed
- ✅ No unresolved discussions
- ✅ Ready for release (if applicable)
- ✅ Branch targets correct base branch (`develop` for features, `main` for hotfixes)

#### 6.2. Opening a Pull Request

**Before opening a Pull Request, ensure you have completed the [Pre-PR Checklist](#61-pre-pr-checklist) above.**

##### PR Title Naming Convention

Pull Request titles must follow the same format as commit messages for consistency:

**Format:**

```
<type>(<optional-scope>): <short imperative description>
```

**Allowed Types:**

- `feat` — new feature
- `fix` — bug fix
- `refactor` — code restructuring
- `docs` — documentation update
- `chore` — maintenance / infrastructure (dependency updates, tooling setup, repository configuration)
- `perf` — performance improvement
- `style` — formatting / lint-only changes
- `ci` — CI/CD pipeline changes (GitHub Actions workflows, CI configuration)
- `test` — adding or updating tests

**Rules:**

- Use imperative mood ("Add…", "Fix…", "Update…")
- Keep it under ~70 characters
- Include issue/ticket IDs when applicable (e.g., `fix(#482): handle null values`)
- Avoid "WIP" in titles — use draft PRs instead
- Use lowercase for type and scope (e.g., `feat(track):`, not `Feat(Track):`)

**Note on Branch Prefixes vs PR Title Types:**

Branch prefixes (`feature/`, `chore/`, `hotfix/`, `release/`) are for branch organization and differ from PR title types:

- Branch `feature/add-flac-support` → PR title: `feat: add flac support` (use `feat`, not `feature`)
- Branch `chore/update-dependencies` → PR title: `chore: update dependencies` (use `chore`)
- Branch `hotfix/critical-bug` → PR title: `fix: critical bug` (use `fix`, not `hotfix`)
- Branch `release/v0.2.1` → PR title: `chore: prepare release v0.2.1` (use `chore`)

**Note on GitHub's Auto-Suggested Titles:**

GitHub automatically generates PR titles based on branch names. **GitHub's auto-suggested titles do not follow our convention**, so you must rewrite them to match the standard format:

- ❌ **GitHub suggestion**: `Feature/add album artist tag support` (from branch `feature/add-album-artist-tag-support`)
- ✅ **Correct format**: `feat(track): add album artist tag support`

- ❌ **GitHub suggestion**: `Chore/format code with ruff` (from branch `chore/format-code-with-ruff`)
- ✅ **Correct format**: `style: format code with ruff`

**Examples:**

- `feat(track): add audio fingerprint support`
- `fix(genre): correctly parse genre hierarchy`
- `docs: update contributing guide`
- `chore: update dependencies`
- `test(track): add test for track upload`
- `fix(#482): handle null search values`
- `style: format code with black`
- `ci: update GitHub Actions workflow`

##### PR Description

When opening a Pull Request, a template will be automatically provided. Ensure your PR description includes:

- ✅ Clear description of changes
- ✅ Reference related issues (e.g., "Fixes #123")
- ✅ Note any breaking changes
- ✅ Include testing instructions if applicable
- ✅ Specify the target branch (`develop` for features, `main` for hotfixes)

**Note:** The PR template (`.github/pull_request_template.md`) will guide you through the process and ensure all necessary information is included.

##### Breaking Changes

If your PR includes breaking changes:

- ✅ Breaking changes are clearly documented in the PR description
- ✅ Migration path is provided (if applicable)
- ✅ Breaking changes include proper versioning notes (for maintainers to handle)

##### PR Automations

When you open a Pull Request, several automations will run automatically:

- **Auto-labeling**: Labels are automatically added based on files changed in your PR:
  - **Component labels**: Automatically applied based on which parts of the codebase you've modified (e.g., `track`, `artist`, `album`, `genre`, `tag`, `playlist`, `play`, `user`, `spotify`, `musicbrainz`, `audio-fingerprinting`, `filtering`, `middleware`, `serializer`, `model`, `view`, `exception`, `utils`)
  - **Type labels**: Automatically applied based on file types (e.g., `test`, `documentation`, `ci`, `dependencies`, `docker`, `scripts`, `migration`, `settings`, `admin`, `fixtures`, `logging`, `management`, `validator`)
  - The labeler configuration is defined in `.github/labeler.yml` and runs via the `.github/workflows/labeler.yml` workflow
  - Multiple labels can be applied to a single PR if it touches multiple areas
- **Manual labels**: You should still add type labels (`bug`, `enhancement`, `feature`) and priority labels manually, as these can't be determined from file paths
- **Auto-assignment**: For contributor PRs (not maintainer PRs), reviewers are automatically assigned
- **CI/CD checks**: Automated tests run on your PR
- **Welcome message**: First-time contributors receive a welcome message with helpful links

These automations help streamline the review process and ensure consistency across the project.

**Note:** If you add a new feature or component, you can suggest updates to `.github/labeler.yml` via a PR to ensure future changes to that component are automatically labeled correctly.

### 7. Releasing _(For Maintainers)_

Releases are created from the `main` branch using **strict Git Flow**.

Quick release process:

1. **Ensure `develop` is ready for release** - All features for the release should be merged into `develop`

   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create a release branch from `develop`**

   ```bash
   git checkout -b release/v0.2.1
   git push origin release/v0.2.1
   ```

3. **On the release branch, prepare the release:**

   - Review and finalize `CHANGELOG.md`:
     - Review changes in the `[Unreleased]` section
     - Move content from `[Unreleased]` section to new version entry with date (e.g., `## [v0.2.1] - 2025-01-15`)
     - Review and consolidate entries if needed
     - Leave the `[Unreleased]` section empty (or with a placeholder) for future PRs

   - Make any final bug fixes or adjustments on the release branch
   - Ensure all tests pass: `pytest`

4. **Merge release branch into `main`**

   ```bash
   git checkout main
   git pull origin main
   git merge --no-ff release/v0.2.1
   git push origin main
   ```

5. **Tag the release on `main`**

   ```bash
   git tag v0.2.1
   git push origin v0.2.1
   ```

   **Important:** The tag version must match the version in `CHANGELOG.md` (with the `v` prefix).

6. **Merge release branch back into `develop`** (to keep develop up to date)

   ```bash
   git checkout develop
   git pull origin develop
   git merge --no-ff release/v0.2.1
   git push origin develop
   ```

7. **Delete the release branch** (locally and remotely)

   ```bash
   git branch -d release/v0.2.1
   git push origin --delete release/v0.2.1
   ```

8. **CI/CD will automatically:**

   - Build Docker images
   - Run tests
   - Deploy if configured

**Hotfix Release Process:**

For urgent production fixes:

1. Create hotfix branch from `main`:

   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-bug-fix
   ```

2. Make the fix and update `CHANGELOG.md` in the `[Unreleased]` section

3. Merge hotfix into `main`:

   ```bash
   git checkout main
   git merge --no-ff hotfix/critical-bug-fix
   git tag v0.2.2  # Increment patch version
   git push origin main --tags
   ```

4. Merge hotfix into `develop`:

   ```bash
   git checkout develop
   git merge --no-ff hotfix/critical-bug-fix
   git push origin develop
   ```

5. Delete the hotfix branch

## 🪪 License & Attribution

All contributions are made under the project's Apache License 2.0.

You retain authorship of your code; the project retains redistribution rights under the same license. See the [LICENSE](LICENSE) file for details.

## 📜 Code of Conduct

This project adheres to a Code of Conduct to ensure a welcoming and inclusive environment for all contributors. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) when participating in this project.

Our Code of Conduct is based on the [Contributor Covenant](https://www.contributor-covenant.org), version 2.1. It outlines our expectations for behavior, unacceptable behavior, and how to report violations.

## 🌍 Contact & Discussions

You can open:

- **Issues** → bug reports or new ideas
  - Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) for reporting bugs
  - Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) for suggesting new features
- **Discussions** → suggestions, architecture, or music-related topics

Let's make this API grow together 🌱

