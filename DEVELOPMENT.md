# Development Guidelines

This document outlines the coding standards and best practices for developing this Django REST API project.

## Table of Contents

- [Code Quality](#code-quality)
  - [General Practices](#general-practices)
  - [Code Style Conventions](#code-style-conventions)
    - [File and Class Naming](#file-and-class-naming)
    - [Field Name Constants](#field-name-constants)
    - [Private Fields](#private-fields)
  - [Docstrings](#docstrings)
    - [When to Add Docstrings](#when-to-add-docstrings)
    - [When NOT to Add Docstrings](#when-not-to-add-docstrings)
  - [Type Checking](#type-checking)
  - [Error Handling](#error-handling)
- [Django Best Practices](#django-best-practices)
  - [Models](#models)
  - [Serializers](#serializers)
  - [Views and ViewSets](#views-and-viewsets)
  - [Filtering](#filtering)
- [API Request Format](#api-request-format)
  - [Multipart Form Data](#multipart-form-data)
- [Project Documentation](#project-documentation)
  - [Documentation Files](#documentation-files)
  - [Code Style Reference](#code-style-reference)

## Code Quality

### General Practices

Follow these code quality standards when developing:

- **Remove commented-out code** - Don't leave commented-out code in the codebase. If code is no longer needed, remove it. Use version control (git) to recover old code if needed.

- **No hardcoded credentials, API keys, or secrets** - Never commit credentials, API keys, passwords, or other sensitive information to the repository. Use environment variables or secure configuration management instead.

- **No debug statements** - Remove all `print()`, `pdb`, `breakpoint()`, and other debug statements before committing.

- **Follow Django best practices** - Use Django's ORM, follow Django conventions, and leverage Django REST Framework features appropriately.

### Code Style Conventions

#### File and Class Naming

All Python files must follow the project's naming conventions:

- **One class per file** - Each file must contain exactly one class (see [One Class Per File](.cursor/rules/one-class-per-file.mdc))

- **Regular classes** (Models, Managers, etc.):
  - Use **PascalCase** for file names
  - File name must match the class name exactly
  - Example: `Genre.py` contains `class Genre(models.Model)`
  - Example: `GenreManager.py` contains `class GenreManager(models.Manager)`

- **Serializer classes**:
  - Use **camelCase** (lowercase) for file names
  - File name should be shorter than the class name
  - Example: `genre.py` contains `class GenreSerializer(serializers.ModelSerializer)`
  - Example: `track.py` contains `class TrackSerializer(serializers.ModelSerializer)`

- **Private modules** can start with `_`:
  - Internal/private modules that are not part of the public API can use a leading underscore prefix
  - Example: `_MetadataManager.py`, `_Id3v2Manager.py`

**Why this matters:**
- Consistent naming makes the codebase easier to navigate
- One class per file improves code organization and maintainability
- Clear distinction between models and serializers through naming

#### Field Name Constants

**Never use string literals for field names.** Always use constants defined in `Fields.py` files located in the same directory as the model/serializer.

- Create a `Fields.py` file in the same directory as your model/serializer
- Define a `Fields` class containing all field name constants with type hints
- Use these constants instead of string literals throughout the codebase

**Good examples:**
```python
# Fields.py
class Fields:
    NAME: str = "name"
    UUID: str = "uuid"
    PARENT: str = "parent"

# Usage in serializer
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = [Fields.NAME, Fields.UUID, Fields.PARENT]

# Usage in view
def get_genre(self, request: Request) -> Response:
    genre = Genre.objects.get(uuid=request.data[Fields.UUID])
    return Response({Fields.NAME: genre.name})
```

**Bad examples:**
```python
# Using string literals
assert result["name"] == "Rock"  # Bad
assert result["parent"] is None  # Bad
```

See [Field Name Constants](.cursor/rules/field-name-constants.mdc) for detailed guidelines.

#### Private Fields

Private fields should start with an underscore to indicate they are internal implementation details.

**Good examples:**
```python
class Genre(models.Model):
    name = models.CharField(max_length=100)  # Public field
    _internal_cache = {}  # Private field
```

### Docstrings

Docstrings should only be added when they provide value (complex logic, public API, edge cases, etc.). When docstrings are needed, use a **systematic Google-style format** for consistency.

#### When to Add Docstrings

- Public API functions/classes (exported from `__init__.py`)
- Complex business logic that isn't obvious
- Functions with non-obvious side effects
- Important edge cases or assumptions
- Django management commands
- Custom exceptions

#### When NOT to Add Docstrings

- Simple getter/setter functions
- Self-explanatory functions with descriptive names
- Test functions (unless testing complex scenarios)
- Internal helper functions that are obvious from context
- Redundant comments that simply restate what the code does

**Example of unnecessary docstring:**
```python
# Bad - Redundant docstring
def get_genre(self, name: str) -> Genre:
    """Get the genre by name."""  # Bad - obvious from method name
    return Genre.objects.get(name=name)
```

See [No Useless Comments](.cursor/rules/no-useless-comments.mdc) for detailed guidelines.

### Type Checking

- **Type hints are encouraged** - Use type hints where appropriate, especially for function parameters and return types
- **Use modern Python type syntax** - Prefer `list`, `dict`, `tuple`, `|` instead of `List`, `Dict`, `Tuple`, `Union` (Python 3.10+)
- **Type hints for public APIs** - All public API functions should have type hints

**Good examples:**
```python
def process_track(track_id: str, user: User) -> dict[str, Any]:
    """Process a track."""
    # Implementation
    return {"status": "processed"}

def get_genres(user: User, name: str | None = None) -> list[Genre]:
    """Get genres for a user."""
    # Implementation
    return genres
```

### Error Handling

- **Use `AppValidationException`** - Never raise DRF validation exceptions directly. Use `AppValidationException` for consistent error handling across the application.

**Good example:**
```python
from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.model.genre.Fields import Fields

def validate_genre_name(self, name: str, user: User) -> None:
    if not name:
        raise AppValidationException(
            field_name=Fields.NAME,
            message="Genre name cannot be empty",
            field_validation_error_code=FieldValidationErrorCode.BLANK
        )
```

**Bad example:**
```python
# Bad - Using DRF ValidationError
from rest_framework.exceptions import ValidationError

def validate_genre_name(self, name: str) -> None:
    if not name:
        raise ValidationError("Genre name cannot be empty")  # Bad
```

See [Use Custom Validation Exception](.cursor/rules/use-custome-validation-exception.mdc) for detailed guidelines.

## Django Best Practices

### Models

- **One class per file** - Each model should be in its own file
- **Use Managers** - Create custom managers when needed for common queries
- **Use field name constants** - Reference fields using constants from `Fields.py`
- **Private resource filtering** - Always include `user` in queries for private resources to ensure proper access control and take advantage of database indexing

**Good example:**
```python
# Genre.py
from bodzify_api.model.genre.Fields import Fields

class Genre(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

# Usage
def get_user_genres(user: User) -> QuerySet:
    return Genre.objects.filter(user=user)  # Good - includes user
```

**Bad example:**
```python
# Bad - Missing user filter
def get_genre(genre_id: UUID) -> Genre:
    return Genre.objects.get(id=genre_id)  # Bad - security risk!
```

See [Private Resource Filtering](.cursor/rules/private-resource-filtering.mdc) for detailed guidelines.

### Serializers

- **One class per file** - Each serializer should be in its own file
- **Use field name constants** - Reference fields using constants from `Fields.py`
- **Use `AppValidationException`** - For validation errors, raise `AppValidationException` instead of DRF's `ValidationError`
- **Inherit from AppInputSerializer** - All **input serializers** (POST, PUT, etc.) should inherit from `AppInputSerializer` (not DRF's `Serializer` directly)
- **Use App fields** - Use `AppCharField`, `AppListField`, etc. instead of DRF's base fields

**AppInputSerializer Overview:**

`AppInputSerializer` extends Django REST Framework's `Serializer` to provide input validation features:
- Consistent error handling using `AppValidationException`
- Multipart form data normalization and validation
- Duplicate field detection (for JSON requests)
- Unknown field detection
- List field handling with `[]` suffix for multipart requests

**Note:** `AppInputSerializer` is specialized for **input validation** (POST, PUT requests). Output serializers (read-only, for GET responses like `*DetailedSerializer`, `*SimpleSerializer`, `*MinimumSerializer`) do not need `AppInputSerializer` and can inherit directly from `serializers.ModelSerializer`.

**Multipart vs JSON Request Handling:**

The serializer handles multipart and JSON requests differently:

1. **List Fields**:
   - **Multipart**: List fields MUST use `[]` suffix (e.g., `artists_names[]`)
   - **JSON**: List fields can be specified without `[]` suffix
   - The serializer automatically maps `[]` suffix fields to their base field names

2. **Field Normalization**:
   - Multipart data is normalized: single values are extracted from lists for non-list fields
   - JSON data is used as-is

3. **Duplicate Field Detection**:
   - **Multipart**: Handled by `DuplicateFieldsMiddleware` before reaching serializer
   - **JSON**: Handled by serializer's `_check_duplicate_fields()` method

**AppField Overview:**

All custom field classes should inherit from `AppField` (not DRF's `Field` directly). `AppField` provides:
- Consistent error handling using `AppValidationException`
- Automatic error code mapping from DRF validation keys
- Proper field name handling for list fields (with `[]` suffix)

**Error Code Mapping:**

`AppField` automatically maps common DRF validation keys to application-specific error codes:
- `'required'` → `FieldValidationErrorCode.REQUIRED`
- `'null'` → `FieldValidationErrorCode.REQUIRED`
- `'blank'` → `FieldValidationErrorCode.BLANK`
- `'invalid'` → `FieldValidationErrorCode.FORMAT_INVALID`
- `'max_length'` → `FieldValidationErrorCode.STRING_TOO_LONG`
- `'min_length'` → `FieldValidationErrorCode.STRING_TOO_SHORT`
- And more (see `AppField.validation_error_code_mapping`)

**Good examples:**

```python
# genre.py
from bodzify_api.model.genre.Fields import Fields
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.field.AppListField import AppListField

class GenreSerializer(AppSerializer):
    name = AppCharField()
    tags = AppListField(child=AppCharField())
    
    class Meta:
        fields = [Fields.NAME, Fields.TAGS]
```

```python
# Custom field example
from bodzify_api.serializer.field.AppField import AppField
from rest_framework import serializers

class AppCharField(AppField, serializers.CharField):
    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('invalid')  # Raises AppValidationException
        return data
```

**Request Format Examples:**

```http
# ✅ Good - Multipart with list field
POST /api/v0.2.0/library/uploaded/
Content-Type: multipart/form-data

title: "Song Title"
artists_names[]: "Artist 1"
artists_names[]: "Artist 2"
```

```json
// ✅ Good - JSON with list field (no [] suffix needed)
POST /api/v0.2.0/library/uploaded/
Content-Type: application/json

{
  "title": "Song Title",
  "artists_names": ["Artist 1", "Artist 2"]
}
```

See `bodzify_api.serializer.AppSerializer` and `bodzify_api.serializer.field.AppField` for detailed implementation documentation.

### Views and ViewSets

- **Use ViewSets** - Prefer ViewSets over function-based views for consistency
- **Use field name constants** - Reference fields using constants from `Fields.py`
- **Proper error handling** - Use `AppValidationException` for validation errors
- **Private resource filtering** - Always include `user` in queries for private resources

### Filtering

- **Use Django Filter** - Leverage django-filter for filtering capabilities
- **Consistent parameters** - Use `ConsistentParametersFilterBackend` for consistent parameter handling
- **Private resource filtering** - Always include `user` in filter queries

## API Request Format

### Multipart Form Data

**Duplicate Field Validation**

According to the HTTP specification (RFC 7578), duplicate field names are standard and allowed in `multipart/form-data`. However, this application enforces a validation rule that **rejects duplicate fields** to prevent confusion and ensure data integrity. This is an application-level constraint, not a protocol requirement.

**Rules:**
- ❌ **Duplicate fields are rejected** - Sending the same field name multiple times will result in a `400 Bad Request` error with error code `duplicate`
- ✅ **List fields are allowed** - Fields with a `[]` suffix (e.g., `artists_names[]`) are allowed to have multiple values, as this is the intended way to send arrays in multipart form data

**Examples:**

```http
# ❌ Bad - Duplicate field
POST /api/v0.2.0/library/uploaded/
Content-Type: multipart/form-data

title: "Song Title 1"
title: "Song Title 2"  # Error: duplicate field

# ✅ Good - Single value
POST /api/v0.2.0/library/uploaded/
Content-Type: multipart/form-data

title: "Song Title"

# ✅ Good - List field with multiple values
POST /api/v0.2.0/library/uploaded/
Content-Type: multipart/form-data

title: "Song Title"
artists_names[]: "Artist 1"
artists_names[]: "Artist 2"
artists_names[]: "Artist 3"
```

**Error Response:**

When duplicate fields are detected, the API returns:

```json
{
  "title": {
    "message": "Duplicate field detected.",
    "code": "duplicate"
  }
}
```

**Implementation:**

Duplicate field detection is handled by `DuplicateFieldsMiddleware` before request data reaches the serializer. For PUT/PATCH requests, the middleware manually parses multipart data since Django doesn't populate `request.POST` for these methods.

See `bodzify_api.middleware.duplicate_fields.middleware.DuplicateFieldsMiddleware` for implementation details.

## Project Documentation

### Documentation Files

When making changes to the codebase, ensure relevant documentation is updated:

- **README.md**: Update when adding new features, changing behavior, or modifying installation/usage instructions
- **CHANGELOG.md**: Always update when creating PRs (see [Changelog Best Practices](CHANGELOG.md#changelog-best-practices) for guidelines)
- **DEVELOPMENT.md**: Update when changing development standards or adding new guidelines
- **CONTRIBUTING.md**: Update when changing development workflow (primarily for maintainers; contributors may update in exceptional cases)
- **code-style.md**: Update when changing code style conventions

**Note:** Documentation should be updated as part of the same PR that introduces the changes, not as a separate follow-up PR.

### Code Style Reference

For quick reference on code style conventions, see [code-style.md](code-style.md). For detailed guidelines, refer to the Cursor rules in `.cursor/rules/`:

- [One Class Per File](.cursor/rules/one-class-per-file.mdc)
- [Field Name Constants](.cursor/rules/field-name-constants.mdc)
- [No Useless Comments](.cursor/rules/no-useless-comments.mdc)
- [Private Resource Filtering](.cursor/rules/private-resource-filtering.mdc)
- [Use Custom Validation Exception](.cursor/rules/use-custome-validation-exception.mdc)
- [Test Structure](.cursor/rules/test-structure.mdc)
- [Test Naming Convention](.cursor/rules/test-naming-convention.mdc)
- [Divide Test Cases](.cursor/rules/divide-test-cases.mdc)
- [Use assert Instead of assertEqual](.cursor/rules/use-assert-not-assertequal.mdc)

