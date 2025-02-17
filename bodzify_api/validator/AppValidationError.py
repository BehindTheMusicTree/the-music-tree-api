from typing import Dict, Any, Union, Optional

from django.core.exceptions import ImproperlyConfigured, ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError

from .FieldValidationErrorCode import FieldValidationErrorCode


class AppValidationError(DrfValidationError):
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
    status_code = 400  # Same as ValidationError
    error_type = 'app_validation_error'  # Marker to identify our error type after DRF processing

    def __init__(self, field: str, message: str, code: FieldValidationErrorCode, source_field=None):
        """
        Initialize AppValidationError with field name and error details.

        Args:
            field: The field name for the error
            message: The error message
            code: The error code
            source_field: Optional source field instance that raised the error.
                         If provided and has get_error_field_name(), that will be used for field name.
        """
        # Use get_error_field_name if available from source field
        self.field = (getattr(source_field, 'get_error_field_name')()
                      if source_field and hasattr(source_field, 'get_error_field_name')
                      else field)
        self.error_detail = {
            'message': message,
            'code': code.value,
            'field': field,  # Always include field name in error detail
            'error_type': 'app_validation_error'  # Add marker in the error detail
        }
        # Store original values for easy access in error handling
        self.original_message = message
        self.original_code = code

        # Always wrap error detail with field name
        error_dict = {field: self.error_detail}
        super().__init__(error_dict)

    @classmethod
    def detect_and_convert_from_drf_error(
            cls, exc: Union[DrfValidationError, DjangoValidationError]) -> Optional['AppValidationError']:
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
        # Convert list to dict if necessary
        if isinstance(detail, list):
            detail = {'error': detail[0] if detail else 'Unknown error'}

        if not isinstance(detail, dict):
            return None

        # Check in field details first
        for field_detail in detail.values():
            if isinstance(field_detail, dict) and field_detail.get('error_type') == cls.error_type:
                return cls.from_drf_validation_error(detail)

        # Then check in top-level detail
        if detail.get('error_type') == cls.error_type:
            return cls.from_drf_validation_error(detail)

        return None

    @classmethod
    def from_drf_validation_error(cls, detail: Dict[str, Any]) -> 'AppValidationError':
        """
        Create an AppValidationError from a DRF ValidationError detail.
        This is used to reconstruct our error format after DRF middleware processing.

        Args:
            detail: The detail dictionary from DRF ValidationError
        """
        if not isinstance(detail, dict):
            raise ImproperlyConfigured('Detail must be a dictionary')

        # Handle field-level validation error
        if 'message' in detail and 'code' in detail:
            # Use preserved field name if available
            field_name = detail.get('field', next(iter(detail)) if len(detail) > 2 else '')
            return cls(
                field=field_name,
                message=str(detail['message']),
                code=FieldValidationErrorCode(str(detail['code']))
            )

        # Handle model/serializer-level validation error
        for field, field_detail in detail.items():
            if isinstance(field_detail, dict) and 'message' in field_detail and 'code' in field_detail:
                # Use preserved field name if available
                field_name = field_detail.get('field', field)
                return cls(
                    field=str(field_name),
                    message=str(field_detail['message']),
                    code=FieldValidationErrorCode(str(field_detail['code']))
                )

        # Fallback for unknown format
        return cls('', str(detail), FieldValidationErrorCode.INVALID_FORMAT)
