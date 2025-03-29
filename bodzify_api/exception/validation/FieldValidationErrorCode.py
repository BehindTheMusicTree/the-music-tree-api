from enum import Enum


class FieldValidationErrorCode(str, Enum):
    DEFAULT = 'validation_error'

    FORMAT_INVALID = 'format_invalid'
    ENUM_INVALID = 'enum_invalid'
    STRING_TOO_LONG = 'string_too_long'
    STRING_TOO_SHORT = 'string_too_short'
    REQUIRED = 'required'
    BLANK = 'blank'
    DUPLICATE = 'duplicate'
    UNKNOWN = 'unknown'
    UNKNOWN_FIELDS = 'fields_unknown'

    # List Validation
    LIST_EXPECTED = 'list_expected'
    LIST_MALFORMED = 'list_malformed'
    LIST_EMPTY = 'list_empty'
    LIST_TOO_LONG = 'list_too_long'
    LIST_TOO_SHORT = 'list_too_short'
    LIST_DUPLICATE_ITEMS = 'list_duplicate_items'
    LIST_ITEM_INVALID = 'list_item_invalid'
    LIST_VALUE_EMPTY = 'list_value_empty'
    LIST_VALUE_DUPLICATE = 'list_value_duplicate'

    # Tree Validation
    TREE_TOO_LONG = 'tree_too_long'
    TREE_MALFORMED = 'tree_malformed'
    TREE_VALUE_DUPLICATE = 'tree_value_duplicate'

    # Reference Validation
    REFERENCE_INVALID = 'reference_invalid'
    SELF_REFERENCE = 'self_reference'
    ANCESTOR_REFERENCE = 'ancestor_reference'

    # File Validation
    FILE_TOO_LARGE = 'file_too_large'
    FILE_TOO_SMALL = 'file_too_small'

    # Audio File Validation
    TRACK_FILE_DOWNLOAD_FAILED = 'track_file_download_failed'
    TRACK_FILE_TYPE_INVALID = 'track_file_type_invalid'
    TRACK_FILE_EXTENSION_INVALID = 'track_file_extension_invalid'
    TRACK_FILE_CORRUPTED = 'track_file_corrupted'
    TRACK_FILE_FINGERPRINT_DUPLICATE = 'track_file_fingerprint_duplicate'

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
