from typing import Any

from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import ValidationError as DrfValidationError

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class AppValidationException(DrfValidationError):
    DEFAULT_FIELD = 'unhandled'  # Default field value when none or empty string provided

    """
    Custom validation error that maintains a consistent structure through DRF's middleware.

    This error always includes:
    - Field name (both in error detail and as dict key)
    - Error type marker (to identify our errors after DRF processing)
    - Message and code

    Error Structure:
        {
            field_name: {
                'message': '...',
                'code': '...',
                'field': field_name,
                'error_type': 'app_validation_error'
            }
        }

    Note on DRF Exception Handling:
    When this exception is raised, DRF's middleware will convert it to a ValidationError instance
    while preserving our error structure. This is expected behavior and our error handling in 
    detect_and_convert_from_drf_error will convert it back to AppValidationError if necessary.

    The error structure is preserved through DRF's middleware by:
    1. Including field name in both the error detail and as dict key
    2. Adding an error_type marker to identify our errors
    3. Using a consistent structure for all validation contexts
    """
    status_code = 400
    error_type = 'app_validation_error'  # Marker to identify our error type after DRF processing

    def __init__(self, message: str,
                 field_validation_error_code: FieldValidationErrorCode,
                 field_name: str | None = DEFAULT_FIELD):
        self.field = field_name if field_name else self.DEFAULT_FIELD
        error_detail = {
            'message': message,
            'code': field_validation_error_code,
            'field': self.field,
            'error_type': self.error_type
        }
        self.errors = {self.field: error_detail}
        super().__init__(self.errors)

    @classmethod
    def detect_and_convert_from_drf_exception(cls, exc: DrfValidationError) -> 'AppValidationException | None':
        """
        Detect if a DRF ValidationError was originally an AppValidationException and convert it back.
        Returns:
            AppValidationError if the error was originally ours, None otherwise
        """
        if not isinstance(exc, DrfValidationError) or not hasattr(exc, 'detail'):
            return None

        detail = exc.detail
        # Convert list to dict if necessary
        if isinstance(detail, list):
            detail = {'error': detail[0] if detail else 'Unknown error'}

        if not isinstance(detail, dict):
            return None

        def has_error_type(error_dict: dict[str, Any]) -> bool:
            """
            Recursively check if the error_type marker exists in the dictionary or its nested values.
            """
            if not isinstance(error_dict, dict):
                return False

            # Check current level
            if error_dict.get('error_type') == cls.error_type:
                return True

            # Check nested dictionaries
            return any(
                has_error_type(value) for value in error_dict.values()
                if isinstance(value, dict)
            )

        # Check if our error_type exists anywhere in the error structure
        if has_error_type(detail):
            return cls.from_drf_validation_error(detail)

        return None

    @classmethod
    def from_drf_validation_error(cls, detail: dict[str, Any]) -> 'AppValidationException':
        """
        Create an AppValidationError from a DRF ValidationError detail.
        This is used to reconstruct our error format after DRF middleware processing.

        Args:
            detail: The detail dictionary from DRF ValidationError

        The method handles three types of validation error structures:
        1. Direct field-level validation error with message and code
        2. Model/serializer-level validation error with nested field details
        3. Deeply nested validation errors (e.g., {'parent': {'parent': {...}}})
        """
        if not isinstance(detail, dict):
            raise ImproperlyConfigured('Detail must be a dictionary')

        def extract_error_details(error_dict: dict[str, Any], parent_field: str = '') -> tuple | None:
            """
            Recursively extract error details from nested dictionaries.
            Returns (field, message, code) tuple if found, None otherwise.
            """
            # Case 1: Direct error details
            if all(key in error_dict for key in ('message', 'code')):
                field = error_dict.get('field', parent_field)
                return (field, str(error_dict['message']), str(error_dict['code']))

            # Case 2 & 3: Nested error details
            for field, field_detail in error_dict.items():
                if isinstance(field_detail, dict):
                    # Recursively check nested dictionary
                    result = extract_error_details(field_detail, field)
                    if result:
                        return result

            return None

        # Try to extract error details from the dictionary
        error_details = extract_error_details(detail)
        if error_details:
            field, message, code = error_details
            return cls(field_name=field, message=message, field_validation_error_code=code)

        # Fallback for unknown format
        return cls(message=str(detail),
                   field_validation_error_code=FieldValidationErrorCode.INVALID_FORMAT,
                   field_name=cls.DEFAULT_FIELD)
