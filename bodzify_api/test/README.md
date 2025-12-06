# Test Structure

This directory contains tests organized into three categories: **unit**, **integration**, and **e2e**.

## Test Categories

### Unit Tests (`unit/`)

Unit tests test individual functions, classes, or modules in isolation with mocked dependencies.

**Location:** `bodzify_api/test/unit/`

**Examples:**
- `unit/utils/audiometa_adapter/` - Tests for audiometa adapter functions
- `unit/utils/file_path_utils/` - Tests for file path utility functions
- `unit/validator/` - Tests for validators

**Characteristics:**
- Fast execution
- No database access
- Mocked external dependencies
- Test single functions/methods

### Integration Tests (`integration/`)

Integration tests test how multiple components work together, typically through API endpoints.

**Location:** `bodzify_api/test/integration/`

**Examples:**
- `integration/view/uploaded_track/` - Tests for uploaded track API endpoints
- Tests that verify metadata reading/writing through the full API stack

**Characteristics:**
- Use database
- Test API endpoints
- Test component interactions
- May use real file operations

### E2E Tests (`e2e/`)

End-to-end tests test complete user workflows and critical paths.

**Location:** `bodzify_api/test/e2e/`

**Examples:**
- Full user workflows (upload → process → retrieve)
- Critical system integrations (audio fingerprinting, Spotify integration)

**Characteristics:**
- Full system tests
- Test complete workflows
- May include external service integrations
- Slower execution

## Running Tests

Run all tests:
```bash
pytest
```

Run specific category:
```bash
pytest bodzify_api/test/unit/
pytest bodzify_api/test/integration/
pytest bodzify_api/test/e2e/
```

Run specific test file:
```bash
pytest bodzify_api/test/unit/utils/audiometa_adapter/test_audiometa_adapter.py
```

## Test Naming Convention

All test functions must follow the pattern: `test_{scenario}_then_{expected_result}`

Examples:
- `test_valid_mp3_extension_then_passes`
- `test_invalid_extension_then_raises_app_validation_exception`
- `test_id3v2_mp3_5_stars_then_10`

## Test Configuration

### Warning Filters

The pytest configuration (`pytest.ini`) includes filters to suppress non-actionable warnings:

- **ResourceWarnings for unclosed files**: Filtered to reduce noise from Django's ORM file handling
  - These warnings occur when Django's ORM accesses `FileField` values internally
  - Django manages these file handles automatically through garbage collection
  - The warnings are non-actionable and originate from Django's internal code, not application code
  - Filter: `ignore:unclosed file:ResourceWarning`

This configuration improves test output clarity while still showing actionable warnings from application code.


