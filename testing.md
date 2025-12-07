# Testing Guidelines

This document outlines testing standards, conventions, and best practices for the project.

For information about development standards, see [Development Guidelines](DEVELOPMENT.md).

## Table of Contents

- [Test Structure](#test-structure)
  - [Test Categories](#test-categories)
  - [Test Location](#test-location)
- [Test Naming Convention](#test-naming-convention)
- [Test Focus and Structure](#test-focus-and-structure)
- [Assertion Style](#assertion-style)
- [Running Tests](#running-tests)
- [External Service Dependencies](#external-service-dependencies)
  - [MusicBrainz ID Retrieval](#musicbrainz-id-retrieval)
- [Test Configuration](#test-configuration)
- [CI Testing](#ci-testing)

## Test Structure

### Test Categories

Tests are organized into three categories: **unit**, **integration**, and **e2e**.

#### Unit Tests (`unit/`)

Unit tests test individual functions, classes, or modules in isolation with mocked dependencies.

**Location:** `api/test/unit/`

**Examples:**
- `unit/utils/audiometa_adapter/` - Tests for audiometa adapter functions
- `unit/utils/file_path_utils/` - Tests for file path utility functions
- `unit/validator/` - Tests for validators

**Characteristics:**
- Fast execution
- No database access
- Mocked external dependencies
- Test single functions/methods

#### Integration Tests (`integration/`)

Integration tests test how multiple components work together, typically through API endpoints.

**Location:** `api/test/integration/`

**Examples:**
- `integration/view/uploaded_track/` - Tests for uploaded track API endpoints
- Tests that verify metadata reading/writing through the full API stack

**Characteristics:**
- Use database
- Test API endpoints
- Test component interactions
- May use real file operations

#### E2E Tests (`e2e/`)

End-to-end tests test complete user workflows and critical paths.

**Location:** `api/test/e2e/`

**Examples:**
- Full user workflows (upload → process → retrieve)
- Critical system integrations (audio fingerprinting, Spotify integration)

**Characteristics:**
- Full system tests
- Test complete workflows
- May include external service integrations
- Slower execution

### Test Location

All tests are located in `api/test/` directory, organized by category.

## Test Naming Convention

All test functions must follow the pattern: `test_{scenario}_then_{expected_result}`

**Components:**
- `scenario`: The scenario being tested, including the action and any relevant conditions (e.g., `import_empty_tree`, `create_genre_with_duplicate_name`, `update_genre_with_invalid_parent`)
- `expected_result`: The expected outcome or error code

**Examples:**
- `test_import_empty_tree_then_400_bad_request`
- `test_create_genre_with_duplicate_name_then_400_bad_request`
- `test_update_genre_with_invalid_parent_then_400_bad_request`
- `test_delete_genre_with_children_then_400_bad_request`
- `test_valid_mp3_extension_then_passes`
- `test_invalid_extension_then_raises_app_validation_exception`

**Guidelines:**
1. Use descriptive names that explain the test's purpose without reading the code
2. Include relevant conditions in the scenario part that make the test case unique
3. For error cases, specify the expected HTTP status code
4. Use underscores to separate words
5. Keep the name concise but informative
6. Avoid generic terms like "test", "check", "verify"
7. Test class names should be descriptive and follow the pattern `Test{Feature}` (e.g., `TestGenreImport`)

**Bad examples:**
- `test_import` (too generic)
- `test_import_tree` (missing conditions and expected result)
- `test_import_with_children` (missing expected result)
- `test_import_fails` (missing specific error condition)
- `TestStuff` (too generic class name)

## Test Focus and Structure

Each test should focus on a single scenario. Large test cases that test multiple scenarios should be divided into multiple focused tests.

**Good examples:**
```python
# Good - Multiple focused tests
def test_empty_name_then_400_bad_request(self):
    tree_data = [{"name": "", "children": []}]
    response = self._post_genres_tree_import(tree_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_duplicate_name_then_400_bad_request(self):
    tree_data = [
        {"name": "Rock", "children": []},
        {"name": "Rock", "children": []}
    ]
    response = self._post_genres_tree_import(tree_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
```

**Bad examples:**
```python
# Bad - Testing multiple scenarios in one test
def test_invalid_input_then_error(self):
    # Test empty name
    tree_data = [{"name": "", "children": []}]
    response = self._post_genres_tree_import(tree_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # Test duplicate name - should be separate test
    tree_data = [
        {"name": "Rock", "children": []},
        {"name": "Rock", "children": []}
    ]
    response = self._post_genres_tree_import(tree_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
```

**Benefits:**
- Easier to identify which specific scenario failed
- Better test isolation
- Clearer test documentation
- Easier test maintenance
- Better test readability
- Faster test execution (can run specific scenarios)
- Easier to debug failures

## Assertion Style

Use the `assert` statement instead of `assertEqual` for better readability and consistency.

**Good examples:**
```python
# Good - Using assert
def test_create_genre(self):
    genre = Genre.objects.create(name="Rock")
    assert genre.name == "Rock"
    assert genre.parent is None
```

**Bad examples:**
```python
# Bad - Using assertEqual
def test_create_genre(self):
    genre = Genre.objects.create(name="Rock")
    self.assertEqual(genre.name, "Rock")  # Bad
    self.assertEqual(genre.parent, None)  # Bad
```

**Guidelines:**
1. Use `assert` for all equality checks
2. Use `assert` with `is` for identity checks
3. Use `assert` with `in` for membership checks
4. Keep assertions simple and readable
5. Use descriptive variable names to make assertions clear

## Running Tests

Run all tests:
```bash
pytest
```

Run specific category:
```bash
pytest api/test/unit/
pytest api/test/integration/
pytest api/test/e2e/
```

Run specific test file:
```bash
pytest api/test/unit/utils/audiometa_adapter/test_audiometa_adapter.py
```

Run specific test:
```bash
pytest api/test/view/track/test_specific.py::TestCase::test_specific_scenario
```

## External Service Dependencies

### MusicBrainz ID Retrieval

Tests that verify MusicBrainz recording ID retrieval should **not fail** when the MusicBrainz lookup fails. MusicBrainz lookups can fail for various reasons unrelated to the application code:

- MusicBrainz service availability
- Network connectivity issues
- Audio fingerprinting service availability
- Temporary service outages
- Rate limiting

**Guidelines:**
- Use `pytest.skip()` instead of `assert` when MusicBrainz recording lookup fails
- Provide descriptive skip messages explaining why the lookup failed
- Check both `musicbrainz_recording_missing_cause` and `fingerprint_missing_cause` to provide context
- This ensures tests don't fail due to external service issues while still validating application logic

**Example:**
```python
def test_drown_7m21_mp3_then_ok(self):
    response = self._post_uploaded_track(
        UploadedTrackTestFilename.RECORDING_JUAN_HANSEN_OOSTIL_DROWN_MASSANO_REMIX_7M21_MP3)
    assert response.status_code == status.HTTP_201_CREATED
    recording = self.saved_object.track_file.musicbrainz_recording
    if not recording:
        missing_cause = self.saved_object.track_file.musicbrainz_recording_missing_cause
        code_label = missing_cause.code.label if missing_cause else "Unknown"
        message = missing_cause.message if missing_cause and missing_cause.message else "No message"
        fingerprint_missing_cause = self.saved_object.track_file.fingerprint_missing_cause
        fingerprint_code_label = fingerprint_missing_cause.code.label if fingerprint_missing_cause else "None"
        pytest.skip(
            f"musicbrainz_recording is None. "
            f"Missing cause: {code_label} - {message}. "
            f"Fingerprint missing cause: {fingerprint_code_label}"
        )
    assert recording
    assert recording.musicbrainz_id == "4a45b00b-273d-40ed-9ecd-42f387f59c22"
```

## Test Configuration

### Warning Filters

The pytest configuration (`pytest.ini`) includes filters to suppress non-actionable warnings:

- **ResourceWarnings for unclosed files**: Filtered to reduce noise from Django's ORM file handling
  - These warnings occur when Django's ORM accesses `FileField` values internally
  - Django manages these file handles automatically through garbage collection
  - The warnings are non-actionable and originate from Django's internal code, not application code
  - Filter: `ignore:unclosed file:ResourceWarning`

This configuration improves test output clarity while still showing actionable warnings from application code.

## CI Testing

- CI runs tests with fail-fast flag (`-x`) - stops on first failure for faster feedback
- Test results are published to GitHub Actions UI
- Tests run automatically on pushes to `main`, `develop`, `release/*`, `hotfix/*` branches and pull requests

