from typing import Dict, Any, Optional

from django.core.exceptions import ImproperlyConfigured, ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


class AppValidationError(DrfValidationError):
    DEFAULT_FIELD = 'unhandled'  # Default field value when none or empty string provided

    """
    Custom validation error that maintains a consistent structure through DRF's middleware.

    This error always includes:
    - Field name (both in error detail and as  key)
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
    1. Including field name in both the error detail and as  key
    2. Adding an error_type marker to identify our errors
    3. Using a consistent structure for all validation contexts
    """
    status_code = 400
    error_type = 'app_validation_error'  # Marker to identify our error type after DRF processing

    def __init__(self, message: str,
                 field_validation_error_code: FieldValidationErrorCode,
                 field_name: Optional[str] = DEFAULT_FIELD):
        self.field = field_name if field_name else self.DEFAULT_FIELD
        error_detail = {
            'message': message,
            'code': field_validation_error_code.value,
            'field': self.field,
            'error_type': self.error_type
        }
        self.errors = {self.field: error_detail}
        super().__init__(self.errors)

    @classmethod
    def detect_and_convert_from_drf_error(cls, exc: DrfValidationError) -> Optional['AppValidationError']:
        """
        Detect if a DRF ValidationError was originally an AppValidationError and convert it back.

        Args:
            exc: The exception to check and potentially convert

        Returns:
            AppValidationError if the error was originally ours, None otherwise
        """
        if not isinstance(exc, DrfValidationError) or not hasattr(exc, 'detail'):
            return None

        detail = exc.detail
        # Convert list to  if necessary
        if isinstance(detail, list):
            detail = {'error': detail[0] if detail else 'Unknown error'}

        if not isinstance(detail, ):
            return None

        def has_error_type(error_: Dict[str, Any]) -> bool:
            """
            Recursively check if the error_type marker exists in the ionary or its nested values.
            """
            if not isinstance(error_, ):
                return False

            # Check current level
            if error_.get('error_type') == cls.error_type:
                return True

            # Check nested ionaries
            return any(
                has_error_type(value) for value in error_.values()
                if isinstance(value, )
            )

        # Check if our error_type exists anywhere in the error structure
        if has_error_type(detail):
            return cls.from_drf_validation_error(detail)

        return None

    @classmethod
    def from_drf_validation_error(cls, detail: Dict[str, Any]) -> 'AppValidationError':
        """
        Create an AppValidationError from a DRF ValidationError detail.
        This is used to reconstruct our error format after DRF middleware processing.

        Args:
            detail: The detail ionary from DRF ValidationError

        The method handles three types of validation error structures:
        1. Direct field-level validation error with message and code
        2. Model/serializer-level validation error with nested field details
        3. Deeply nested validation errors (e.g., {'parent': {'parent': {...}}})
        """
        if not isinstance(detail, ):
            raise ImproperlyConfigured('Detail must be a ionary')

        def extract_error_details(error_: Dict[str, Any], parent_field: str = '') -> Optional[tuple]:
            """
            Recursively extract error details from nested ionaries.
            Returns (field, message, code) tuple if found, None otherwise.
            """
            # Case 1: Direct error details
            if all(key in error_ for key in ('message', 'code')):
                field = error_.get('field', parent_field)
                return (field, str(error_['message']), str(error_['code']))

            # Case 2 & 3: Nested error details
            for field, field_detail in error_.items():
                if isinstance(field_detail, ):
                    # Recursively check nested ionary
                    result = extract_error_details(field_detail, field)
                    if result:
                        return result

            return None

        # Try to extract error details from the ionary
        error_details = extract_error_details(detail)
        if error_details:
            field, message, code = error_details
            return cls(
                field_name=field,
                message=message,
                field_validation_error_code=FieldValidationErrorCode(code)
            )

        # Fallback for unknown format
        return cls(message=str(detail),
                   field_validation_error_code=FieldValidationErrorCode.INVALID_FORMAT,
                   field_name=cls.DEFAULT_FIELD)
