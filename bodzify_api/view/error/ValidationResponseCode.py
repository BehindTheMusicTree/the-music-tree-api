from enum import Enum


class ValidationResponseCode(Enum):
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
    FIELD_SELF_REFERENCE = 2106
    FIELD_ANCESTOR_REFERENCE = 2107
    FIELD_FILE_TOO_LARGE = 2108
    FIELD_FILE_TOO_SMALL = 2109
    FIELD_INVALID_FILE_TYPE = 2110
    FIELD_INVALID_FILENAME = 2111
    FIELD_INVALID_URL = 2112
    FIELD_URL_NOT_FOUND = 2113
    FIELD_URL_REQUEST_FAILED = 2114
    """
    # Field validation (conceptually 2100-2199)
    FIELD_BLANK = 'blank'
    FIELD_INVALID_ENUM = 'invalid_enum'
    FIELD_REQUIRED = 'required'
    FIELD_INVALID_FORMAT = 'invalid_format'
    FIELD_INVALID_CHOICE = 'invalid_choice'
    FIELD_SELF_REFERENCE = 'self_reference'
    FIELD_ANCESTOR_REFERENCE = 'ancestor_reference'
    FIELD_FILE_TOO_LARGE = 'file_too_large'
    FIELD_FILE_TOO_SMALL = 'file_too_small'
    FIELD_INVALID_FILE_TYPE = 'invalid_file_type'
    FIELD_INVALID_FILENAME = 'invalid_filename'
    FIELD_INVALID_URL = 'invalid_url'
    FIELD_URL_NOT_FOUND = 'url_not_found'
    FIELD_URL_REQUEST_FAILED = 'url_request_failed'
