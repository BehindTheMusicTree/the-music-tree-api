from enum import Enum


class FieldValidationErrorCode(Enum):
    """
    Enumerated validation response codes for field validation errors.
    These codes are used specifically for field-level validation responses.

    While the codes are stored as strings for Django compatibility,
    they conceptually map to the 2100-2199 range for field-specific validation errors:

    FIELD_BLANK = 2101
    FIELD_INVALID_ENUM = 2102
    FIELD_REQUIRED = 2103
    FIELD_INVALID_FORMAT = 2104
    FIELD_INVALID_CHOICE = 2105
    FIELD_UNKNOWN = 2106          # Single unknown field
    FIELD_UNKNOWN_MULTIPLE = 2107  # Multiple unknown fields found
    FIELD_SELF_REFERENCE = 2108
    FIELD_ANCESTOR_REFERENCE = 2109
    FIELD_FILE_TOO_LARGE = 2108
    FIELD_FILE_TOO_SMALL = 2109
    FIELD_INVALID_FILE_TYPE = 2110
    FIELD_INVALID_FILENAME = 2111
    FIELD_INVALID_URL = 2112
    FIELD_URL_NOT_FOUND = 2113
    FIELD_URL_REQUEST_FAILED = 2114
    FIELD_INVALID_FILTER = 2115
    FIELD_DUPLICATE_FINGERPRINT = 2116
    FIELD_FILE_CORRUPTED = 2117
    FIELD_METADATA_EXTRACTION_FAILED = 2118
    FIELD_NAME_EMPTY = 2119
    FIELD_NAME_DUPLICATE = 2120
    FIELD_DB_INTEGRITY_ERROR = 2121
    """
    # Field validation (conceptually 2100-2199)
    FIELD_BLANK = 'blank'
    FIELD_INVALID_ENUM = 'invalid_enum'
    FIELD_REQUIRED = 'required'
    FIELD_INVALID_FORMAT = 'invalid_format'
    FIELD_INVALID_CHOICE = 'invalid_choice'
    FIELD_UNKNOWN = 'unknown_field'
    FIELD_UNKNOWN_MULTIPLE = 'unknown_fields'
    FIELD_SELF_REFERENCE = 'self_reference'
    FIELD_ANCESTOR_REFERENCE = 'ancestor_reference'
    FIELD_FILE_TOO_LARGE = 'file_too_large'
    FIELD_FILE_TOO_SMALL = 'file_too_small'
    FIELD_INVALID_FILE_TYPE = 'invalid_file_type'
    FIELD_INVALID_FILENAME = 'invalid_filename'
    FIELD_INVALID_URL = 'invalid_url'
    FIELD_URL_NOT_FOUND = 'url_not_found'
    FIELD_URL_REQUEST_FAILED = 'url_request_failed'
    FIELD_INVALID_FILTER = 'invalid_filter'
    FIELD_DUPLICATE_FINGERPRINT = 'duplicate_fingerprint'
    FIELD_FILE_CORRUPTED = 'file_corrupted'
    FIELD_METADATA_EXTRACTION_FAILED = 'metadata_extraction_failed'
    FIELD_NAME_EMPTY = 'name_empty'
    FIELD_NAME_DUPLICATE = 'name_duplicate'
    FIELD_NAMES_DUPLICATE = 'names_duplicate'
    FIELD_DB_INTEGRITY_ERROR = 'db_integrity_error'
    FIELD_PLAYLIST_NAME_DUPLICATE = 'playlist_name_duplicate'
    FIELD_MUTUALLY_EXCLUSIVE = 'mutually_exclusive'
    FIELD_DEPENDENCY_MISSING = 'dependency_missing'
    FIELD_RESOURCE_NOT_OWNED = 'resource_not_owned'
    FIELD_NO_UPDATES = 'no_updates'  # Used when a PUT request contains no fields to update
    # When an artist name is empty in a list of multiple artists
    FIELD_ARTIST_NAME_EMPTY_IN_LIST = 'artist_name_empty_in_list'
    FIELD_ARTIST_NAMES_DUPLICATE = 'artist_names_duplicate'  # When duplicate artist names are provided
