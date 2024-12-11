
from typing import List, Dict, Any, Union
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


def raise_duplicate_fields_error(fields: List[str]) -> None:
    """Raise a validation error for duplicate fields."""
    raise ValidationError({
        'duplicate_fields': {
            'code': 'duplicate_fields',
            'message': f'Duplicate fields found: {", ".join(fields)}',
            'fields': fields
        }
    })


def raise_integrity_error(exc: IntegrityError, error_code: str) -> None:
    """Raise a ValidationError from an IntegrityError."""
    raise ValidationError({
        'integrity_error': {
            'message': str(exc),
            'code': error_code.lower()
        }
    })


def raise_validation_error(message: str, code: str, field: Union[str, None] = None) -> None:
    """Raise a ValidationError with the given message and code."""
    error_detail: Dict[str, Any] = {
        'message': message,
        'code': code
    }

    if field is not None:
        raise ValidationError({field: error_detail})
    else:
        raise ValidationError(error_detail)


def raise_unknown_fields_error(fields: List[str]) -> None:
    """Raise a validation error for unknown fields."""
    raise ValidationError({
        'unknown_fields': {
            'code': 'unknown_fields',
            'message': f'Unknown fields found: {", ".join(fields)}',
            'fields': fields
        }
    })


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
                'code': error.get('code', 'invalid'),
                **{k: v for k, v in error.items() if k not in ['message', 'code']}
            }
            for error in field_errors
        ]
        for field, field_errors in errors.items()
    }

    raise ValidationError({'errors': formatted_errors})


def handle_drf_validation_error(exc: ValidationError, error_code: str) -> None:
    """Handle a DRF ValidationError and re-raise it in our standard format."""
    if isinstance(exc.detail, dict):
        # Get the first error from the dictionary
        first_field = next(iter(exc.detail.keys()))
        first_error = exc.detail[first_field]
        if isinstance(first_error, (list, tuple)):
            first_error = first_error[0]
        raise_validation_error(
            message=str(first_error),
            code=error_code.lower(),
            field=str(first_field)
        )
    elif isinstance(exc.detail, (list, tuple)):
        first_error = exc.detail[0]
        raise_validation_error(message=str(first_error), code=error_code.lower())
    else:
        raise_validation_error(message=str(exc.detail), code=error_code.lower())
