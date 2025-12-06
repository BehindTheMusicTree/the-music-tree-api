# Architecture Overview

This document describes the architectural patterns, design decisions, and system structure of the Bodzify API Django application.

## Table of Contents

- [Overview](#overview)
- [Request Processing Pipeline](#request-processing-pipeline)
  - [API Request Format](#api-request-format)
    - [Multipart Form Data](#multipart-form-data)
- [Core Architectural Patterns](#core-architectural-patterns)
  - [Models](#models)
  - [Serializers](#serializers)
  - [Views and ViewSets](#views-and-viewsets)
  - [Middleware](#middleware)
  - [Filtering](#filtering)
  - [Error Handling](#error-handling)

## Overview

The Bodzify API is built on Django REST Framework and follows a layered architecture with clear separation of concerns:

1. **Request Layer**: Middleware handles request preprocessing and validation
2. **View Layer**: ViewSets handle HTTP methods and orchestrate business logic
3. **Serializer Layer**: Serializers handle data validation, transformation, and serialization
4. **Model Layer**: Django models represent the data structure and business logic
5. **Filter Layer**: Custom filter backends handle query parameter filtering

## Request Processing Pipeline

The request processing pipeline follows this flow:

1. **HTTP Request Reception** - Django receives the raw HTTP request
2. **Middleware Processing** - Multiple middleware layers transform and validate the data
3. **DRF Parsing** - Django REST Framework parses the request body
4. **View Processing** - ViewSets handle routing and business logic
5. **Serializer Validation** - Custom serializers validate and normalize the data
6. **Model Operations** - Database operations are performed
7. **Response Serialization** - Data is serialized for the response

For detailed information about the input data flow, see [Input Data Flow documentation](input-data-flow.md).

### API Request Format

#### Multipart Form Data

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

## Core Architectural Patterns

### Models

**Base Model Hierarchy:**

The application uses a hierarchical model structure with base classes for common patterns:

- **BaseModel**: Base class for all models with common fields (UUID, timestamps)
- **PrivateStandardResource**: Models that belong to users and support standard CRUD operations
- **PrivateUniqueResource**: Models that belong to users and enforce uniqueness constraints
- **PublicStandardResource**: Models that are shared across users
- **PublicUniqueResource**: Models that are shared and enforce uniqueness

**Key Patterns:**

- **One class per file** - Each model is in its own file following the class name
- **Use Managers** - Create custom managers when needed for common queries
- **Field name constants** - All field names are defined in `Fields.py` files in the same directory
- **Private resource filtering** - All private resources include `user` in queries for access control and indexing
- **UUID primary keys** - Models use UUID as primary keys for better distribution and security

**Best Practices:**

**Good example:**
```python
# Genre.py
from bodzify_api.model.genre.Fields import Fields

class Genre(PrivateStandardResource):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    
    class Meta:
        indexes = [
            models.Index(fields=[Fields.USER, Fields.NAME]),
        ]

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

**Guidelines:**

- Always include `user` in queries for private resources to ensure proper access control and take advantage of database indexing
- Use field name constants from `Fields.py` instead of string literals
- Create custom managers for common query patterns
- Define database indexes that include `user` as the first field for private resources

### Serializers

**Serializer Hierarchy:**

- **AppInputSerializer**: Base class for all input serializers (POST, PUT, PATCH)
- **ModelSerializer**: Base class for output serializers (GET responses)
- **AppField**: Base class for all custom field types

**Key Patterns:**

- **One class per file** - Each serializer is in its own file
- **Input vs Output separation** - Input serializers inherit from `AppInputSerializer`, output serializers from `ModelSerializer`
- **AppField pattern** - All custom fields inherit from `AppField` for consistent error handling
- **Field name constants** - Use `Fields` constants instead of string literals
- **Multipart support** - Handles both multipart/form-data and JSON requests
- **List field handling** - Multipart requests require `[]` suffix for list fields
- **Use `AppValidationException`** - For validation errors, raise `AppValidationException` instead of DRF's `ValidationError`

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
- Consistent error handling using `AppValidationException` (for input validation)
- Automatic error code mapping from DRF validation keys
- Proper field name handling for list fields (with `[]` suffix)

**Note:** `AppField` fields can be used in both input and output serializers. The validation error handling is only triggered during input validation (`to_internal_value`). For output serializers, fields are used for serialization (`to_representation`) only.

**Error Code Mapping:**

`AppField` automatically maps common DRF validation keys to application-specific error codes:
- `'required'` → `FieldValidationErrorCode.REQUIRED`
- `'null'` → `FieldValidationErrorCode.REQUIRED`
- `'blank'` → `FieldValidationErrorCode.BLANK`
- `'invalid'` → `FieldValidationErrorCode.FORMAT_INVALID`
- `'max_length'` → `FieldValidationErrorCode.STRING_TOO_LONG`
- `'min_length'` → `FieldValidationErrorCode.STRING_TOO_SHORT`
- And more (see `AppField.validation_error_code_mapping`)

**Best Practices:**

**Good examples:**

```python
# genre.py
from bodzify_api.model.genre.Fields import Fields
from bodzify_api.serializer.AppInputSerializer import AppInputSerializer
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.field.AppListField import AppListField

class GenreSerializer(AppInputSerializer):
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

For detailed information about serializer patterns and input data flow, see [Input Data Flow documentation](input-data-flow.md).

### Views and ViewSets

**ViewSet Hierarchy:**

- **AppModelViewSet**: Base ViewSet for model-based endpoints with standard CRUD operations
- **SearchViewSet**: Specialized ViewSet for multi-model search functionality

**Key Patterns:**

- **Use ViewSets** - Prefer ViewSets over function-based views for consistency
- **Generic ViewSets** - Use `AppModelViewSet` for standard CRUD operations
- **Serializer selection** - Views use different serializers for different operations (create, update, list, retrieve)
- **Private resource filtering** - All private resource views filter by user
- **Consistent filter backend** - All views use `ConsistentParametersFilterBackend` for query parameter handling
- **Pagination** - Standard pagination using `AppPagination`
- **Use field name constants** - Reference fields using constants from `Fields.py`
- **Proper error handling** - Use `AppValidationException` for validation errors

**Best Practices:**

**Example:**

```python
class GenreViewSet(AppModelViewSet[Genre]):
    def __init__(self, **kwargs):
        super().__init__(
            model_class=Genre,
            filterset_class=GenreFilterSet,
            detailed_serializer_class=GenreDetailedSerializer,
            simple_serializer_class=GenreSimpleSerializer,
            **kwargs
        )
```

**Guidelines:**

- Always use `AppModelViewSet` for standard CRUD operations
- Configure serializers for different operations (create, update, list, retrieve)
- Always include `user` in queries for private resources
- Use field name constants from `Fields.py` instead of string literals
- Raise `AppValidationException` for validation errors, never DRF's `ValidationError`

### Middleware

**Middleware Pipeline:**

The middleware processes requests in this order:

1. **ContentTypeValidationMiddleware** - Validates Content-Type headers
2. **CamelToSnakeMiddleware** - Converts camelCase to snake_case
3. **ContentValidityMiddleware** - Validates request content structure
4. **TestClientEmptyListMiddleware** - Handles test client empty list normalization
5. **ListValueValidationMiddleware** - Validates list field values
6. **DuplicateFieldsMiddleware** - Detects and rejects duplicate fields

**Key Patterns:**

- **Early validation** - Middleware validates requests before they reach views
- **Request transformation** - Middleware transforms request data (camelCase conversion, normalization)
- **Error handling** - Middleware raises `AppValidationException` for invalid requests
- **Test client support** - Special handling for Django test client limitations

For detailed information about middleware processing, see [Input Data Flow documentation](input-data-flow.md).

### Filtering

**Filter Backend:**

- **ConsistentParametersFilterBackend**: Custom filter backend that ensures consistent parameter handling with pagination

**Key Patterns:**

- **FilterSet classes** - Views define `filterset_class` to specify available filters
- **Explicit rejection** - Views without `filterset_class` reject filter parameters with `AppValidationException`
- **Pagination parameters** - `page` and `page_size` are excluded from filter validation
- **Private resource filtering** - All filters include user in the query for access control

**Behavior:**

The `ConsistentParametersFilterBackend` ensures consistent parameter handling with pagination. If a view does not define a `filterset_class` and filter parameters are provided, this backend raises an `AppValidationException` with `FieldValidationErrorCode.INVALID_FILTER`. This ensures that invalid filter usage is rejected explicitly rather than silently ignored, providing clear feedback to API clients about unsupported filter parameters.

**Example:**

```python
class GenreFilterSet(AppFilterSet):
    name = AppFilter(field_name=Fields.NAME)
    
    class Meta:
        model = Genre
        fields = [Fields.NAME]
```

### Error Handling

**Error Exception Hierarchy:**

- **AppValidationException**: Base exception for all validation errors
- **FieldValidationErrorCode**: Enum of validation error codes

**Key Patterns:**

- **Consistent error format** - All validation errors use `AppValidationException` with field name, message, and error code
- **No DRF exceptions** - Never raise DRF's `ValidationError` directly
- **Field-specific errors** - Errors include the field name that caused the error
- **Error code mapping** - `AppField` automatically maps DRF validation keys to application error codes

**Error Response Format:**

```json
{
  "field_name": {
    "message": "Error message",
    "code": "error_code"
  }
}
```

**Best Practices:**

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

**Guidelines:**

- Always use `AppValidationException` instead of DRF's `ValidationError`
- Include all required parameters: `field_name`, `message`, and `field_validation_error_code`
- Use field name constants from `Fields.py` instead of string literals
- Use appropriate error codes from `FieldValidationErrorCode` enum