from enum import Enum


class FieldValidationErrorCode(Enum):
    """
    Enumerated validation response codes for field validation errors.
    These codes are used specifically for field-level validation responses.

    While the codes are stored as strings for Django compatibility,
    they conceptually map to the 2100-2199 range for field-specific validation errors.

    Field Validation Codes (2100-2199):
        BLANK = 2101                    # Empty field when value required
        INVALID_ENUM = 2102             # Invalid enumeration value
        REQUIRED = 2103                 # Missing required field
        INVALID_FORMAT = 2104           # Field format validation failed
        INVALID_CHOICE = 2105           # Invalid choice from available options
        UNKNOWN = 2106                  # Single unknown field
        UNKNOWN_MULTIPLE = 2107         # Multiple unknown fields found
        SELF_REFERENCE = 2108           # Field references itself
        ANCESTOR_REFERENCE = 2109       # Invalid ancestor reference
        FILE_TOO_LARGE = 2110          # File size exceeds limit
        FILE_TOO_SMALL = 2111          # File size below minimum
        INVALID_FILE_TYPE = 2112       # Unsupported file type
        INVALID_FILENAME = 2113        # Invalid filename format
        INVALID_URL = 2114             # Malformed URL
        URL_NOT_FOUND = 2115           # URL resource not found
        URL_REQUEST_FAILED = 2116      # URL request failed
        INVALID_FILTER = 2117          # Invalid filter parameters
        DUPLICATE_FINGERPRINT = 2118   # Duplicate audio fingerprint
        FILE_CORRUPTED = 2119          # File integrity check failed
        METADATA_EXTRACTION_FAILED = 2120 # Failed to extract metadata
        NAME_EMPTY = 2121              # Empty name field
        NAME_DUPLICATE = 2122          # Duplicate name
        NAMES_DUPLICATE = 2123         # Multiple duplicate names
        DB_INTEGRITY_ERROR = 2124      # Database integrity violation
        PLAYLIST_NAME_DUPLICATE = 2125  # Duplicate playlist name
        MUTUALLY_EXCLUSIVE = 2126      # Mutually exclusive fields
        DEPENDENCY_MISSING = 2127      # Required dependent field missing
        RESOURCE_NOT_OWNED = 2128      # Resource ownership validation failed
        NO_UPDATES = 2129              # No fields to update
        ARTIST_NAME_EMPTY_IN_LIST = 2130 # Empty artist name in list
        ARTIST_NAMES_DUPLICATE = 2131   # Duplicate artist names
        POSITION_IN_ALBUM_TOO_SMALL = 2132 # Album position below minimum
        POSITION_IN_ALBUM_TOO_LARGE = 2133 # Album position exceeds maximum
        RATING_TOO_SMALL = 2134        # Rating below minimum
        RATING_TOO_LARGE = 2135        # Rating exceeds maximum
    """
    # Basic field validation
    BLANK = 'blank'
    INVALID_ENUM = 'invalid_enum'
    REQUIRED = 'required'
    INVALID_FORMAT = 'invalid_format'
    INVALID_CHOICE = 'invalid_choice'
    FIELD_DUPLICATE = 'field_duplicate'

    # Field existence validation
    UNKNOWN = 'unknown_field'
    UNKNOWN_MULTIPLE = 'unknown_fields'

    # Reference validation
    SELF_REFERENCE = 'self_reference'
    ANCESTOR_REFERENCE = 'ancestor_reference'

    # File validation
    FILE_TOO_LARGE = 'file_too_large'
    FILE_TOO_SMALL = 'file_too_small'
    INVALID_FILE_TYPE = 'invalid_file_type'
    INVALID_FILENAME = 'invalid_filename'

    # URL validation
    INVALID_URL = 'invalid_url'
    URL_NOT_FOUND = 'url_not_found'
    URL_REQUEST_FAILED = 'url_request_failed'

    # Filter and fingerprint validation
    INVALID_FILTER = 'invalid_filter'
    DUPLICATE_FINGERPRINT = 'duplicate_fingerprint'

    # File processing validation
    FILE_CORRUPTED = 'file_corrupted'
    METADATA_EXTRACTION_FAILED = 'metadata_extraction_failed'

    # Name validation
    NAME_EMPTY = 'name_empty'
    NAME_DUPLICATE = 'name_duplicate'
    NAMES_DUPLICATE = 'names_duplicate'

    # Database validation
    DB_INTEGRITY_ERROR = 'db_integrity_error'

    # Playlist validation
    PLAYLIST_NAME_DUPLICATE = 'playlist_name_duplicate'

    # Field relationship validation
    MUTUALLY_EXCLUSIVE = 'mutually_exclusive'
    DEPENDENCY_MISSING = 'dependency_missing'
    RESOURCE_NOT_OWNED = 'resource_not_owned'
    NO_UPDATES = 'no_updates'

    # Artist validation
    ARTIST_NAME_EMPTY_IN_LIST = 'artist_name_empty_in_list'
    ARTIST_NAMES_DUPLICATE = 'artist_names_duplicate'

    # Album position validation
    POSITION_IN_ALBUM_TOO_SMALL = 'position_in_album_too_small'
    POSITION_IN_ALBUM_TOO_LARGE = 'position_in_album_too_large'

    # Rating validation
    RATING_TOO_SMALL = 'rating_too_small'
    RATING_TOO_LARGE = 'rating_too_large'