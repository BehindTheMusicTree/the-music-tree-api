from typing import Dict, Any, Union, Optional

from django.core.exceptions import ImproperlyConfigured, ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError

from .FieldValidationErrorCode import FieldValidationErrorCode


class AppValidationError(DrfValidationError):
    """
    Custom validation error that maintains its class through DRF middleware.
    Instead of inheriting from ValidationError, we implement the DRF exception interface.
    """
    status_code = 400  # Same as ValidationError
    error_type = 'app_validation_error'  # Marker to identify our error type after DRF processing
    """
    Custom validation error that maintains a consistent structure across different validation contexts.
    
    Note on DRF Exception Handling:
    When this exception is raised, DRF's middleware will convert it to a ValidationError instance
    while preserving our error structure. This is expected behavior and our error handling in 
    ErrorResponse.from_validation_error is designed to work with this conversion.

    Error Structure:
        Field-level validation (from_field, from_filter):
            {'message': '...', 'code': '...'}  # DRF wraps with field name
            Used in: to_internal_value, validate_<field>, filter methods

        Other validation (from_serializer, from_model, from_middleware, from_filterset):
            {'field_name': {'message': '...', 'code': '...'}}  # We wrap with field name
            Used in: validate methods, model validation, middleware, filterset validation

    Factory Methods:
        from_field: Field-level validation (DRF handles field wrapping)
        from_filter: Filter field validation (DRF handles field wrapping)
        from_serializer: Serializer-level validation
        from_model: Model-level validation (e.g., integrity errors)
        from_middleware: Middleware-level validation
        from_filterset: Filterset-level validation
    """

    def __init__(self, field: str, message: str, code: FieldValidationErrorCode):
        self.field = field
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

        print('exception:', exc)

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
