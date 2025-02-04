import re
import inspect
from typing import List, Dict, Any, Optional
from rest_framework.exceptions import ValidationError

from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


# Regex pattern to extract field name from constraint names
CONSTRAINT_FIELD_PATTERN = re.compile(r'(?:non_empty_|unique_)(\w+)(?:_per_user)?')


def raise_validation_error(message: str, field_validation_error_code: FieldValidationErrorCode, field: str) -> None:
    """
    Raise a validation error with a specific field and error details.

    Args:
        message: Human-readable error message
        field_validation_error_code: Machine-readable error code
        field: The field that caused the validation error

    Note:
        In field validation context (run_validation method), DRF automatically wraps the error
        with the field name, so we pass the error detail directly:
            ValidationError({'message': '...', 'code': '...'})
            -> DRF wraps it as: {'field_name': {'message': '...', 'code': '...'}}

        In serializer context, we need to wrap the error with the field name ourselves:
            ValidationError({'field_name': {'message': '...', 'code': '...'}})

        This way we work with DRF's validation chain instead of against it, letting DRF
        handle field wrapping in field validation context while we handle it in serializer context.
    """
    error_detail = {
        'message': message,
        'code': field_validation_error_code.value
    }

    # In field validation context (run_validation), let DRF handle field wrapping
    if 'run_validation' in inspect.stack()[1].function:
        # DRF will automatically wrap this with the field name
        raise ValidationError(error_detail)
    else:
        # In serializer context, wrap with field name ourselves
        raise ValidationError({field: error_detail})


def raise_duplicate_field_error(field: str) -> None:
    error_detail: Dict[str, Any] = {
        'message': f'Duplicate field found',
        'code': FieldValidationErrorCode.FIELD_NAME_DUPLICATE.value,
    }
    raise ValidationError({field: error_detail})


def raise_duplicate_fields_error(fields: List[str]) -> None:
    error_detail: Dict[str, Any] = {
        'message': f'Duplicate fields found: {", ".join(fields)}',
        'code': FieldValidationErrorCode.FIELD_NAMES_DUPLICATE.value,
    }
    raise ValidationError({'duplicate_fields': error_detail})


def raise_unknown_field_error(field: str) -> None:
    """
    Raise a validation error for a single unknown field.

    Args:
        field: The name of the field that was not recognized in the request
    """
    raise_validation_error(
        message='Unrecognized field',
        field_validation_error_code=FieldValidationErrorCode.FIELD_UNKNOWN,
        field=field
    )


def raise_unknown_fields_error(fields: List[str]) -> None:
    """
    Raise a validation error for multiple unknown fields.
    The error includes both a descriptive message and the list of unknown fields.

    Args:
        fields: List of field names that were not recognized in the request
    """
    if len(fields) == 1:
        raise_unknown_field_error(fields[0])
        return

    error_detail: Dict[str, Any] = {
        'message': 'Request contains multiple unrecognized fields',
        'code': FieldValidationErrorCode.FIELD_UNKNOWN_MULTIPLE.value,
        'fields': fields
    }
    raise ValidationError({'unknown_fields': error_detail})


def raise_multiple_validation_errors(errors: Dict[str, List[Dict[str, Any]]]) -> None:
    """
    Raise a ValidationError with multiple field errors.

    Args:
        errors: A dictionary where keys are field names and values are lists of error details.
               Each error detail should be a dictionary containing at least 'message' and 'code'.

    Example:
        raise_multiple_validation_errors({
            'email': [
                {
                    'message': 'Email is already taken',
                    'code': 'unique'
                },
                {
                    'message': 'Email is invalid',
                    'code': 'invalid'
                }
            ],
            'password': [
                {
                    'message': 'Password must be at least 8 characters',
                    'code': 'min_length',
                    'min_length': 8  # Additional context can be included
                }
            ]
        })

    Response Format:
    {
        "errors": {
            "email": [
                {
                    "message": "Email is already taken",
                    "code": "unique"
                },
                {
                    "message": "Email is invalid",
                    "code": "invalid"
                }
            ],
            "password": [
                {
                    "message": "Password must be at least 8 characters",
                    "code": "min_length",
                    "min_length": 8
                }
            ]
        }
    }
    """
    formatted_errors = {
        field: [
            {
                'message': error.get('message', 'Validation error occurred'),
                'code': error.get('code', FieldValidationErrorCode.FIELD_INVALID_FORMAT.value),
                **{k: v for k, v in error.items() if k not in ['message', 'code']}
            }
            for error in field_errors
        ]
        for field, field_errors in errors.items()
    }

    raise ValidationError({'errors': formatted_errors})