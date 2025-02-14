from typing import Dict, Any
from rest_framework.exceptions import ValidationError

from .FieldValidationErrorCode import FieldValidationErrorCode


class AppValidationError(ValidationError):
    """
    Custom validation error that maintains its class through DRF middleware.
    Instead of inheriting from ValidationError, we implement the DRF exception interface.
    """
    status_code = 400  # Same as ValidationError
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

    def __init__(self, field: str, message: str, code: FieldValidationErrorCode, is_field_level_validation: bool = False):
        self.field = field
        self.error_detail = {
            'message': message,
            'code': code.value
        }
        # Store original values for easy access in error handling
        self.original_message = message
        self.original_code = code
        self.is_field_level_validation = is_field_level_validation

        # Create the error structure based on context
        error_dict = self.error_detail if is_field_level_validation else {field: self.error_detail}
        # Add a marker to identify this as AppValidationError even after DRF processing
        self.is_app_validation_error = True
        super().__init__(error_dict)

    @classmethod
    def from_field(cls, field: str, message: str, code: FieldValidationErrorCode) -> 'AppValidationError':
        """
        Create a field-level validation error (e.g., from to_internal_value or validate_<field>).
        DRF will handle the field wrapping automatically in field validation context.
        """
        return cls(field, message, code, is_field_level_validation=True)

    @classmethod
    def from_serializer(cls, field: str, message: str, code: FieldValidationErrorCode) -> 'AppValidationError':
        """
        Create a serializer-level validation error (e.g., from validate method).
        Wraps the error with field name since we're outside field validation context.
        """
        return cls(field, message, code, is_field_level_validation=False)

    @classmethod
    def from_model(cls, field: str, message: str, code: FieldValidationErrorCode) -> 'AppValidationError':
        """
        Create a model-level validation error (e.g., from save method or integrity errors).
        Wraps the error with field name since model validation is similar to serializer validation.
        """
        return cls(field, message, code, is_field_level_validation=False)

    @classmethod
    def from_filter(cls, field: str, message: str, code: FieldValidationErrorCode) -> 'AppValidationError':
        """
        Create a filter-level validation error (e.g., from filter method).
        DRF will handle the field wrapping automatically in filter validation context.
        """
        return cls(field, message, code, is_field_level_validation=True)

    @classmethod
    def from_middleware(cls, field: str, message: str, code: FieldValidationErrorCode) -> 'AppValidationError':
        """
        Create a middleware-level validation error (e.g., from request processing).
        Wraps the error with field name since middleware validation is outside DRF's field context.
        """
        return cls(field, message, code, is_field_level_validation=False)

    @classmethod
    def from_filterset(cls, field: str, message: str, code: FieldValidationErrorCode) -> 'AppValidationError':
        """
        Create a filterset-level validation error (e.g., from filterset validation).
        Wraps the error with field name since filterset validation is similar to serializer validation.
        """
        return cls(field, message, code, is_field_level_validation=False)

    def get_error_detail(self) -> Dict[str, Any]:
        """Get the error detail in a consistent format."""
        return self.error_detail

    @classmethod
    def from_drf_validation_error(cls, detail: Dict[str, Any]) -> 'AppValidationError':
        """
        Create an AppValidationError from a DRF ValidationError detail.
        This is used to reconstruct our error format after DRF middleware processing.

        Args:
            detail: The detail dictionary from DRF ValidationError
        """
        if not isinstance(detail, dict):
            return cls('', str(detail), FieldValidationErrorCode.VALIDATION_ERROR, True)

        # Handle field-level validation error
        if 'message' in detail and 'code' in detail:
            field_name = next(iter(detail)) if len(detail) > 2 else ''
            return cls(
                field=field_name,
                message=str(detail['message']),
                code=FieldValidationErrorCode(str(detail['code'])),
                is_field_level_validation=True
            )

        # Handle model/serializer-level validation error
        for field, field_detail in detail.items():
            if isinstance(field_detail, dict) and 'message' in field_detail and 'code' in field_detail:
                return cls(
                    field=str(field),
                    message=str(field_detail['message']),
                    code=FieldValidationErrorCode(str(field_detail['code'])),
                    is_field_level_validation=False
                )

        # Fallback for unknown format
        return cls('', str(detail), FieldValidationErrorCode.INVALID_FORMAT, True)
