from enum import Enum


class FieldValidationErrorCode(str, Enum):
    """
    Enumerated validation response codes for field validation errors.
    These codes are used specifically for field-level validation responses.

    While the codes are stored as strings for Django compatibility,
    they conceptually map to specific validation categories:

    General Validation:
        DEFAULT = 2100                  # Generic validation error

    Field Content Validation:
        BLANK = 2101                    # Empty field when value required
        REQUIRED = 2102                 # Missing required field
        INVALID_FORMAT = 2103           # Field format validation failed
        INVALID_ENUM = 2104             # Invalid enumeration value
        STRING_TOO_LONG = 2105          # String exceeds maximum length
        STRING_TOO_SHORT = 2106         # String below minimum length
        FIELD_DUPLICATE = 2107          # Duplicate field value

    Field Structure Validation:
        UNKNOWN_FIELD = 2110            # Single unknown field
        UNKNOWN_FIELDS = 2111           # Multiple unknown fields

    list Validation:
        LIST_EXPECTED = 2121            # Single value when list expected
        MALFORMED_LIST = 2122           # Malformed list structure (e.g., missing [] suffix)
        LIST_EMPTY = 2123               # list is empty when values required
        LIST_TOO_LONG = 2124            # list exceeds maximum length
        LIST_TOO_SHORT = 2125           # list below minimum length
        LIST_DUPLICATE_ITEMS = 2126     # list contains duplicate items
        LIST_ITEM_INVALID = 2127        # Individual list item is invalid

    Reference Validation:
        INVALID_REFERENCE = 2130        # Invalid reference to another entity
        SELF_REFERENCE = 2131           # Field references itself
        ANCESTOR_REFERENCE = 2132       # Invalid ancestor reference

    File Validation:
        FILE_TOO_LARGE = 2140          # File size exceeds limit
        FILE_TOO_SMALL = 2141          # File size below minimum
        INVALID_FILE_TYPE = 2142        # Unsupported file type
        INVALID_FILENAME = 2143         # Invalid filename format
        FILE_CORRUPTED = 2144          # File integrity check failed
        DUPLICATE_FINGERPRINT = 2145    # Duplicate audio fingerprint
        METADATA_EXTRACTION_FAILED = 2146 # Failed to extract metadata

    URL Validation:
        INVALID_URL = 2150             # Malformed URL
        URL_NOT_FOUND = 2151           # URL resource not found
        URL_REQUEST_FAILED = 2152      # URL request failed

    Name Validation:
        NAME_EMPTY = 2160              # Empty name field
        NAME_DUPLICATE = 2161          # Duplicate name
        ARTIST_NAME_EMPTY_IN_LIST = 2162 # Empty artist name in list
        ARTIST_NAMES_DUPLICATE = 2163   # Duplicate artist names

    Resource Validation:
        RESOURCE_NOT_OWNED = 2170      # Resource ownership validation failed
        NO_UPDATES = 2171              # No fields to update
        MUTUALLY_EXCLUSIVE = 2172      # Mutually exclusive fields
        DEPENDENCY_MISSING = 2173      # Required dependent field missing

    Numeric Range Validation:
        TRACK_NUMBER_TOO_SMALL = 2180 # Album position below minimum
        TRACK_NUMBER_TOO_LARGE = 2181 # Album position exceeds maximum
        RATING_TOO_SMALL = 2182        # Rating below minimum
        RATING_TOO_LARGE = 2183        # Rating exceeds maximum

    Filter Validation:
        INVALID_FILTER = 2190          # Single invalid filter
        INVALID_FILTERS = 2191         # Multiple invalid filters

    Database Validation:
        DB_INTEGRITY_ERROR = 2195      # Database integrity violation
    """

    # General Validation
    DEFAULT = 'validation_error'

    # Field Content Validation
    FORMAT_INVALID = 'format_invalid'
    ENUM_INVALID = 'enum_invalid'
    STRING_TOO_LONG = 'string_too_long'
    STRING_TOO_SHORT = 'string_too_short'
    REQUIRED = 'required'
    BLANK = 'blank'
    DUPLICATE = 'duplicate'
    UNKNOWN = 'unknown'
    UNKNOWN_FIELDS = 'fields_unknown'

    # list Validation
    LIST_EXPECTED = 'list_expected'
    LIST_MALFORMED = 'list_malformed'
    LIST_EMPTY = 'list_empty'
    LIST_TOO_LONG = 'list_too_long'
    LIST_TOO_SHORT = 'list_too_short'
    LIST_DUPLICATE_ITEMS = 'list_duplicate_items'
    LIST_ITEM_INVALID = 'list_item_invalid'
    LIST_VALUE_EMPTY = 'list_value_empty'
    LIST_VALUE_DUPLICATE = 'list_value_duplicate'

    # Reference Validation
    REFERENCE_INVALID = 'reference_invalid'
    SELF_REFERENCE = 'self_reference'
    ANCESTOR_REFERENCE = 'ancestor_reference'

    # File Validation
    FILE_TOO_LARGE = 'file_too_large'
    FILE_TOO_SMALL = 'file_too_small'

    # Audio File Validation
    AUDIO_FILE_DOWNLOAD_FAILED = 'audio_file_download_failed'
    AUDIO_FILE_TYPE_INVALID = 'audio_file_type_invalid'
    AUDIO_FILE_EXTENSION_INVALID = 'audio_file_extension_invalid'
    AUDIO_FILE_CORRUPTED = 'audio_file_corrupted'
    AUDIO_FILE_FINGERPRINT_DUPLICATE = 'audio_file_fingerprint_duplicate'

    # URL Validation
    URL_INVALID = 'url_invalid'
    URL_NOT_FOUND = 'url_not_found'
    URL_REQUEST_FAILED = 'url_request_failed'

    # Name Validation
    NAME_EMPTY = 'name_empty'
    NAME_DUPLICATE = 'name_duplicate'

    # Resource Validation
    RESOURCE_NOT_OWNED = 'resource_not_owned'
    NO_UPDATES = 'no_updates'
    MUTUALLY_EXCLUSIVE = 'mutually_exclusive'
    DEPENDENCY_MISSING = 'dependency_missing'

    # Numeric Range Validation
    TRACK_NUMBER_TOO_SMALL = 'track_number_too_small'
    TRACK_NUMBER_TOO_LARGE = 'track_number_too_large'
    RATING_TOO_SMALL = 'rating_too_small'
    RATING_TOO_LARGE = 'rating_too_large'

    # Filter Validation
    INVALID_FILTER = 'invalid_filter'
    INVALID_FILTERS = 'invalid_filters'

    # Database Validation
    DB_INTEGRITY_ERROR = 'db_integrity_error'

    def __str__(self) -> str:
        return str(self.value)
