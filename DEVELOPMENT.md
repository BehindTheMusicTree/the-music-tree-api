# Development Guidelines

This document outlines the coding standards and best practices for developing this Django REST API project.

For information about system architecture, patterns, and design decisions, see [Architecture documentation](docs/ARCHITECTURE.md).

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
- [Architecture](#architecture)
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

- **Use `AppValidationException`** - Never raise DRF validation exceptions directly. Use `AppValidationException` for consistent error handling across the application

For detailed information about error handling architecture, patterns, and examples, see [Architecture documentation](docs/ARCHITECTURE.md#error-handling).

See [Use Custom Validation Exception](.cursor/rules/use-custome-validation-exception.mdc) for detailed guidelines.

## Architecture

For comprehensive information about system architecture, Django best practices, and design patterns, see [Architecture documentation](docs/ARCHITECTURE.md).

The architecture documentation covers:

- **Request Processing Pipeline** - How requests flow through the system
- **Core Architectural Patterns** - Models, Serializers, Views, Middleware, Filtering, and Error Handling
- **Django Best Practices** - Detailed patterns, examples, and guidelines for each component
- **Related Documentation** - Links to input data flow and other architectural resources

For API request format specifications, including multipart form data handling and duplicate field validation, see [Architecture documentation](docs/ARCHITECTURE.md#api-request-format).

## Project Documentation

### Documentation Files

When making changes to the codebase, ensure relevant documentation is updated:

- **README.md**: Update when adding new features, changing behavior, or modifying installation/usage instructions
- **CHANGELOG.md**: Always update when creating PRs (see [Changelog Best Practices](CHANGELOG.md#changelog-best-practices) for guidelines)
- **DEVELOPMENT.md**: Update when changing development standards or adding new guidelines
- **CONTRIBUTING.md**: Update when changing development workflow (primarily for maintainers; contributors may update in exceptional cases)
- **code-style.md**: Update when changing code style conventions

**Note:** Documentation should be updated as part of the same PR that introduces the changes, not as a separate follow-up PR.

### Architecture Documentation

For detailed documentation on system architecture, patterns, and design decisions:

- **Architecture Overview**: [Architecture documentation](docs/ARCHITECTURE.md) - Architectural patterns, design decisions, and system structure
- **Input Data Flow**: [Input Data Flow documentation](docs/input-data-flow.md) - How input data flows from HTTP request reception through middleware processing to final validation in serializers

### External Service Documentation

For detailed documentation on external service integrations, see:

- **MusicBrainz Integration**: [MusicBrainz Integration documentation](bodzify_api/utils/musicbrainz/README.md) - Audio fingerprinting and MusicBrainz metadata lookup
- **Spotify Integration**: [Spotify Integration documentation](bodzify_api/utils/spotify_api/README.md) - Spotify Web API integration
- **Audio Metadata**: [Audio Metadata Handling documentation](bodzify_api/utils/audio_file_metadata/README.md) - Audio file metadata reading and writing

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

