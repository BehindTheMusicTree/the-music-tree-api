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
    """
    # Field validation (conceptually 2100-2199)
    FIELD_BLANK = 'blank'
    FIELD_INVALID_ENUM = 'invalid_enum'
    FIELD_REQUIRED = 'required'
    FIELD_INVALID_FORMAT = 'invalid_format'
    FIELD_INVALID_CHOICE = 'invalid_choice'