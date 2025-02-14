from typing import Dict, Any
from rest_framework.exceptions import ValidationError

from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


class AppValidationError(ValidationError):
    """
    Custom validation error that maintains a consistent structure across different validation contexts.
    Each factory method corresponds to a specific validation context and ensures proper error structure.

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
