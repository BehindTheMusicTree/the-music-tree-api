# Input Data Flow: From Reception to Validation

This document describes how input data flows from HTTP request reception through middleware processing to final validation in serializers.

## Table of Contents

- [Overview](#overview)
- [Request Reception](#request-reception)
- [Middleware Processing](#middleware-processing)
  - [Middleware Order](#middleware-order)
  - [ContentTypeValidationMiddleware](#contenttypevalidationmiddleware)
  - [CamelToSnakeMiddleware](#cameltosnakemiddleware)
  - [ContentValidityMiddleware](#contentvaliditymiddleware)
  - [TestClientEmptyListMiddleware](#testclientemptylistmiddleware)
  - [ListValueValidationMiddleware](#listvaluevalidationmiddleware)
  - [DuplicateFieldsMiddleware](#duplicatefieldsmiddleware)
- [DRF Parsing](#drf-parsing)
  - [Parsers](#parsers)
  - [Parsing Behavior](#parsing-behavior)
  - [Lazy Parsing](#lazy-parsing)
- [Serializer Validation](#serializer-validation)
  - [AppInputSerializer](#appinputserializer)
  - [Data Flow in Serializer](#data-flow-in-serializer)
  - [Multipart Normalization](#multipart-normalization)
  - [Test Client Empty List Normalization](#test-client-empty-list-normalization)
- [Complete Flow Examples](#complete-flow-examples)
  - [POST Request (Multipart)](#post-request-multipart)
  - [PUT Request (Multipart)](#put-request-multipart)
  - [JSON Request](#json-request)
- [Key Differences: POST vs PUT/PATCH](#key-differences-post-vs-putpatch)
- [Test Client Special Handling](#test-client-special-handling)
- [Field Name Conventions](#field-name-conventions)
- [Error Handling](#error-handling)

## Overview

The input data processing pipeline consists of several stages:

1. **HTTP Request Reception** - Django receives the raw HTTP request
2. **Middleware Processing** - Multiple middleware layers transform the data
3. **DRF Parsing** - Django REST Framework parses the request body
4. **Serializer Validation** - Custom serializers validate and normalize the data

## Request Reception

When a request arrives, Django creates an `HttpRequest` object containing:
- `request.body` - Raw request body bytes
- `request.META` - HTTP headers and metadata
- `request.POST` - Form data (populated by Django for POST requests only)
- `request.FILES` - Uploaded files
- `request.GET` - Query parameters

For PUT/PATCH requests, Django does **not** populate `request.POST` - the data must be parsed from `request.body`.

## Middleware Processing

Middleware processes requests in the order defined in `settings.py`. Each middleware can modify the request before it reaches the view.

### Middleware Order

1. `SecurityMiddleware` - Security headers
2. `CorsMiddleware` - CORS handling
3. `SessionMiddleware` - Session management
4. `HostValidationMiddleware` - Host validation
5. `CommonMiddleware` - Common utilities
6. `ContentTypeValidationMiddleware` - Content-Type validation and JSON structure validation
7. `CamelToSnakeMiddleware` - Field name conversion (camelCase → snake_case)
8. `ContentValidityMiddleware` - Content validity and parsing validation
9. `TestClientEmptyListMiddleware` - Empty list normalization (test client only)
10. `ListValueValidationMiddleware` - List value validation (rejects empty values mixed with non-empty)
11. `DuplicateFieldsMiddleware` - Duplicate field detection
12. `RequestLoggingMiddleware` - Request logging
13. `CsrfViewMiddleware` - CSRF protection
14. `AuthenticationMiddleware` - Authentication
15. `MessageMiddleware` - Messages framework
16. `XFrameOptionsMiddleware` - Clickjacking protection

### ContentTypeValidationMiddleware

**Purpose**: Validates Content-Type header and JSON request structure.

**Processing**:
- **Content-Type validation**: Ensures Content-Type header is present and supported
- **JSON structure validation**: 
  - Rejects double-encoded JSON strings (e.g., `"{\"key\": \"value\"}"`)
  - Rejects JSON arrays as root (e.g., `["Muse", ""]`) - API expects objects
  - Validates UTF-8 encoding

**Example**:
```python
# ✅ Valid: {"artistName": "Muse"}
# ❌ Invalid: ["Muse", ""]  # Arrays rejected
# ❌ Invalid: "{\"key\": \"value\"}"  # Double-encoded rejected
```

### CamelToSnakeMiddleware

**Purpose**: Converts camelCase field names to snake_case for consistency.

**Processing**:
- **JSON requests**: Parses JSON body, converts field names, sets `request.data` directly
- **Multipart POST requests**: Converts `request.POST` field names (Django populates this)
- **Multipart PUT/PATCH requests**: Does not process (Django doesn't populate `request.POST` for these methods)
- **GET requests**: Converts query parameter field names

**Example**:
```python
# Input: {"artistName": "Muse"}
# Output: {"artist_name": "Muse"}
```

### ContentValidityMiddleware

**Purpose**: Validates that request data is accessible and properly parsed.

**Processing**:
- **JSON requests**: Validates that `request.data` is accessible after `CamelToSnakeMiddleware`
- **Multipart POST requests**: Validates that `request.POST` is accessible
- **Multipart PUT/PATCH requests**: Validates that `request.data` can be accessed (DRF will parse it)
- **Rejects requests**: If accessing request data raises an exception, rejects with `400 ParseError`

**Example**:
```python
# If request.data access fails → 400 ParseError: "Failed to parse request data..."
# If request.POST access fails → 400 ParseError: "Failed to parse multipart form data..."
```

**Note**: This middleware ensures that parsing failures are caught early and rejected, rather than allowing malformed requests to reach validation middleware or serializers.

### TestClientEmptyListMiddleware

**Purpose**: Normalizes empty list fields for test client requests.

**Problem**: DRF's test client drops empty lists (`[]`) in multipart form data. To preserve them, `AppApiClient` converts `[]` to `['']` for list fields. This middleware normalizes `['']` back to `[]`.

**Processing**:
- **POST requests**: Normalizes `request.POST` directly (after `CamelToSnakeMiddleware`)
- **PUT/PATCH requests**: Not handled in middleware (see Serializer Processing)

**Example**:
```python
# Input: {"artists_names[]": ['']}
# Output: {"artists_names[]": []}
```

**Note**: Only processes requests marked with `X-Test-Client: true` header.

### ListValueValidationMiddleware

**Purpose**: Detects and rejects list fields containing both empty and non-empty values.

**Processing**:
- **POST requests**: Validates `request.POST` for multipart requests (after TestClientEmptyListMiddleware normalization)
- **PUT/PATCH requests**: Manually parses multipart data to validate
- **JSON requests**: Validates `request.data` (after ContentValidityMiddleware ensures it's accessible)
- **Validation rule**: List fields cannot contain both empty values (`''`, `None`) and non-empty values

**Example**:
```python
# ✅ Valid: {"artists_names[]": ["Muse", "Radiohead"]}  # All non-empty
# ✅ Valid: {"artists_names[]": []}  # All empty
# ❌ Invalid: {"artists_names[]": ["Muse", ""]}  # Mixed empty and non-empty
```

**Note**: This validation is also performed at the field level (`ArtistsNamesField`) as a fallback for defense in depth. ContentValidityMiddleware ensures parsing failures are rejected before reaching this middleware.

### DuplicateFieldsMiddleware

**Purpose**: Detects and rejects duplicate fields in multipart/form-data requests.

**Processing**:
- **POST requests**: Checks `request.POST` for duplicates
- **PUT/PATCH requests**: Manually parses multipart data to detect duplicates
- **Exception**: List fields with `[]` suffix are allowed to have multiple values

## DRF Parsing

Django REST Framework parses the request body lazily when `request.data` is first accessed. The parser is selected based on the `Content-Type` header.

### Parsers

- **JSONParser**: Parses `application/json` requests
- **MultiPartParser**: Parses `multipart/form-data` requests
- **FormParser**: Parses `application/x-www-form-urlencoded` requests

### Parsing Behavior

- **JSON**: Returns a Python `dict`
- **Multipart**: Returns a `QueryDict` (Django's dictionary-like object for form data)
- **Form**: Returns a `QueryDict`

### Lazy Parsing

DRF uses lazy parsing - `request.data` is only parsed when first accessed. This means:
- Middleware that accesses `request.data` triggers parsing
- The parsed data is cached in `request._full_data`
- Subsequent accesses return the cached data

## Serializer Validation

The serializer receives the parsed data and performs validation and normalization.

### AppInputSerializer

The base serializer for all input validation. It handles:

1. **Malformed Array Detection**: Detects list fields without `[]` suffix in multipart requests
2. **Unknown Field Detection**: Detects fields not defined in the serializer
3. **Multipart Normalization**: Extracts single values from lists for non-list fields
4. **Test Client Empty List Normalization**: Converts `['']` back to `[]` for test client requests
5. **Duplicate Field Checking**: Verifies no duplicate fields exist
6. **Field Validation**: Validates individual fields
7. **Object Validation**: Validates the entire object

### Data Flow in Serializer

```python
def run_validation(self, data):
    # 1. Check for malformed arrays and unknown fields
    _, unknown_fields = self._collect_known_fields_and_malformed_array_fields_names(data)
    
    # 2. Normalize multipart data (extract single values from lists)
    if is_multipart:
        data = self._normalize_multipart_data(data)
    
    # 3. Normalize test client empty lists ([''] → [])
    if is_test_client:
        data = self._normalize_test_client_empty_lists(data)
    
    # 4. Check for duplicate fields
    self._check_duplicate_fields(...)
    
    # 5. Validate fields
    validated_data = self._validate_fields(data)
    
    # 6. Validate object
    validated_data = self._validate_object(validated_data)
    
    return validated_data
```

### Multipart Normalization

For multipart form data, the serializer normalizes the structure:

- **List fields** (with `[]` suffix): Kept as lists
- **Non-list fields**: Single values extracted from lists

**Example**:
```python
# Input QueryDict: {"title": ["My Title"], "artists_names[]": ["Muse", "Radiohead"]}
# Output: {"title": "My Title", "artists_names[]": ["Muse", "Radiohead"]}
```

### Test Client Empty List Normalization

For test client requests, the serializer normalizes empty list fields:

**Example**:
```python
# Input: {"artists_names[]": ['']}
# Output: {"artists_names[]": []}
```

**Why in serializer?**: 
- DRF parses `request.data` lazily, making middleware interception complex
- Overriding `request.data` in middleware is unreliable due to DRF's internal caching
- The serializer already has the parsed data at the right point in validation

## Complete Flow Examples

### POST Request (Multipart)

1. **Request Reception**: Django receives multipart/form-data
2. **ContentTypeValidationMiddleware**: Validates Content-Type header
3. **CamelToSnakeMiddleware**: Converts `request.POST` field names to snake_case
4. **ContentValidityMiddleware**: Validates that `request.POST` is accessible
5. **TestClientEmptyListMiddleware**: Normalizes `['']` to `[]` in `request.POST` (test client only)
6. **ListValueValidationMiddleware**: Validates list values
7. **DRF Parsing**: When serializer accesses `request.data`, DRF uses `request.POST` (already normalized)
8. **Serializer Validation**: Validates and normalizes the data

### PUT Request (Multipart)

1. **Request Reception**: Django receives multipart/form-data
2. **ContentTypeValidationMiddleware**: Validates Content-Type header
3. **CamelToSnakeMiddleware**: Does not process (no `request.POST` for PUT)
4. **ContentValidityMiddleware**: Validates that `request.data` can be accessed (DRF will parse it)
5. **TestClientEmptyListMiddleware**: Does not process (handled in serializer)
6. **ListValueValidationMiddleware**: Manually parses multipart data to validate list values
7. **DRF Parsing**: When serializer accesses `request.data`, DRF parses from `request.body`
8. **Serializer Validation**: 
   - Normalizes multipart data structure
   - Normalizes test client empty lists (`['']` → `[]`)
   - Validates fields

### JSON Request

1. **Request Reception**: Django receives JSON body
2. **ContentTypeValidationMiddleware**: Validates Content-Type and JSON structure (rejects arrays, double-encoded JSON)
3. **CamelToSnakeMiddleware**: Parses JSON, converts field names, sets `request.data` directly
4. **ContentValidityMiddleware**: Validates that `request.data` is accessible (rejects if parsing failed)
5. **ListValueValidationMiddleware**: Validates list values
6. **DRF Parsing**: `request.data` already set by middleware (no lazy parsing)
7. **Serializer Validation**: Validates the data

## Key Differences: POST vs PUT/PATCH

| Aspect | POST | PUT/PATCH |
|--------|------|-----------|
| `request.POST` | Populated by Django | Empty |
| CamelCase conversion | Via `request.POST` | Via `request.data` (in serializer) |
| Empty list normalization | Via `request.POST` (middleware) | Via `request.data` (serializer) |
| DRF parsing | Uses `request.POST` | Parses from `request.body` |

## Test Client Special Handling

Test client requests are marked with `X-Test-Client: true` header. Special handling includes:

1. **AppApiClient**: Converts `[]` to `['']` for list fields in multipart requests
2. **TestClientEmptyListMiddleware**: Normalizes `['']` back to `[]` for POST requests
3. **AppInputSerializer**: Normalizes `['']` back to `[]` for PUT/PATCH requests

This workaround is necessary because DRF's test client drops empty lists in multipart form data.

## Field Name Conventions

- **JSON requests**: Use camelCase (e.g., `artistName`)
- **Multipart requests**: Use snake_case with `[]` suffix for lists (e.g., `artists_names[]`)
- **Internal processing**: All field names converted to snake_case

## Error Handling

Validation errors are raised as `AppValidationException` with:
- `field_name`: The field that caused the error
- `message`: Human-readable error message
- `field_validation_error_code`: Specific error code (enum)

Common error codes:
- `UNKNOWN`: Unknown field
- `LIST_MALFORMED`: List field without `[]` suffix
- `LIST_VALUE_EMPTY`: Empty value in list
- `NAME_DUPLICATE`: Duplicate field name

