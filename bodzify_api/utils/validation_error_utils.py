
import re
from typing import List, Dict, Any, Union
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from bodzify_api.view.error.ValidationResponseCode import ValidationResponseCode


# Regex pattern to extract field name from constraint names
CONSTRAINT_FIELD_PATTERN = re.compile(r'(?:non_empty_|unique_)(\w+)(?:_per_user)?')


def raise_validation_error(message: str, code: Union[str, ValidationResponseCode], field: str) -> None:
    """
    Raise a validation error with a specific field and error details.

    Args:
        message: Human-readable error message
        code: Machine-readable error code
        field: The field that caused the validation error
    """
    error_detail: Dict[str, Any] = {
        'message': message,
        'code': code.value if isinstance(code, ValidationResponseCode) else code
    }
    raise ValidationError({field: error_detail})


def raise_duplicate_fields_error(fields: List[str]) -> None:
    error_detail: Dict[str, Any] = {
        'message': f'Duplicate fields found: {", ".join(fields)}',
        'code': ValidationResponseCode.FIELD_NAME_DUPLICATE.value,
        'fields': fields
    }
    raise ValidationError({'duplicate_fields': error_detail})


def raise_integrity_error(exc: IntegrityError, error_code: Union[str, ValidationResponseCode, None] = None) -> None:
    """
    Raise a validation error for a database integrity error that is caused by user input.
    This should ONLY be used at the model level for known constraint violations that represent
    validation failures (like unique constraints or non-empty checks).

    Error Handling Pattern:
    1. Model Level (e.g., in model.save()):
       - Catch specific integrity errors that represent validation failures
       - Use raise_validation_error with specific codes (FIELD_NAME_DUPLICATE, FIELD_NAME_EMPTY)
       - Let unknown integrity errors propagate up

    2. View Level (RequestHandler, AppModelViewSet):
       - Handle validation errors (DrfValidationError, DjangoValidationError)
       - Treat unhandled integrity errors as system errors
       - Use ErrorResponse.from_unhandled_integrity_error for system-level integrity errors

    Example from Criteria model:
        try:
            model.save()
        except IntegrityError as e:
            if 'non_empty_name' in str(e):
                raise_validation_error(
                    message='Name cannot be empty',
                    code=ValidationResponseCode.FIELD_NAME_EMPTY.value,
                    field='name'
                )
            elif 'unique_name_per_user' in str(e):
                raise_validation_error(
                    message='A criteria with this name already exists',
                    code=ValidationResponseCode.FIELD_NAME_DUPLICATE.value,
                    field='name'
                )
            # Let other database integrity errors propagate to be handled as system errors
            raise e

    Args:
        exc: The integrity error from the database
        error_code: The specific validation code for known constraint violations.
                   Use FIELD_NAME_DUPLICATE for unique constraints,
                   FIELD_NAME_EMPTY for non-empty constraints, etc.
                   Defaults to FIELD_DB_INTEGRITY_ERROR for general integrity errors.
    """
    error_msg = str(exc)

    # Try to extract field name from constraint name
    match = CONSTRAINT_FIELD_PATTERN.search(error_msg)
    if match:
        field = match.group(1)
    # Try to determine the type of constraint if field name couldn't be extracted
    elif 'unique constraint' in error_msg.lower():
        field = 'unknown_unique_field'
    elif 'not null constraint' in error_msg.lower():
        field = 'unknown_required_field'
    elif 'foreign key constraint' in error_msg.lower():
        field = 'unknown_reference_field'
    else:
        field = 'unknown_constraint_field'

    raise_validation_error(
        message=error_msg,
        code=error_code if error_code is not None else ValidationResponseCode.FIELD_DB_INTEGRITY_ERROR.value,
        field=field
    )


def raise_unknown_fields_error(fields: List[str]) -> None:
    raise_validation_error(
        message=f'Unknown fields found: {", ".join(fields)}',
        code=ValidationResponseCode.FIELD_INVALID_CHOICE.value,
        field='unknown_fields'
    )


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
                'code': error.get('code', ValidationResponseCode.FIELD_INVALID_FORMAT.value),
                **{k: v for k, v in error.items() if k not in ['message', 'code']}
            }
            for error in field_errors
        ]
        for field, field_errors in errors.items()
    }

    raise ValidationError({'errors': formatted_errors})


def handle_drf_validation_error(exc: ValidationError, error_code: Union[str, ValidationResponseCode]) -> None:
    """Handle a DRF ValidationError and re-raise it in our standard format."""
    if isinstance(exc.detail, dict):
        # Get the first error from the dictionary
        first_field = next(iter(exc.detail.keys()))
        first_error = exc.detail[first_field]
        if isinstance(first_error, (list, tuple)):
            first_error = first_error[0]
        raise_validation_error(
            message=str(first_error),
            code=error_code.value if isinstance(error_code, ValidationResponseCode) else error_code.lower(),
            field=str(first_field)
        )
    elif isinstance(exc.detail, (list, tuple)):
        first_error = exc.detail[0]
        raise_validation_error(
            message=str(first_error),
            code=error_code.value if isinstance(error_code, ValidationResponseCode) else error_code.lower(),
            field='validation_error'
        )
    else:
        raise_validation_error(
            message=str(exc.detail),
            code=error_code.value if isinstance(error_code, ValidationResponseCode) else error_code.lower(),
            field='validation_error'
        )
