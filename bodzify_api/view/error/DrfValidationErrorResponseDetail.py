
from dataclasses import dataclass
from typing import Any, Dict

from rest_framework.exceptions import ErrorDetail as DRFErrorDetail

"""
Error Response Detail Module

This module provides a standardized way to format error responses in the API.
The error format follows these conventions:

1. Basic Field Validation Error:
{
    "field_name": {
        "message": "Human readable error message",
        "code": "machine_readable_code",
        "details": {
            "value": "invalid value",
            "requirement": "validation requirement"
        }
    }
}

2. Multiple Errors on Single Field:
{
    "password": {
        "message": "Password validation failed",
        "code": "invalid_password",
        "details": {
            "errors": [
                {
                    "message": "Password is too short",
                    "code": "min_length",
                    "min_length": "8"
                },
                {
                    "message": "Password must contain a number",
                    "code": "password_complexity"
                }
            ]
        }
    }
}

3. Unknown/Invalid Fields Error:
{
    "unknown_fields": {
        "message": "Unknown field(s) detected: sort_by, invalid_filter",
        "code": "invalid_fields",
        "details": {
            "fields": ["sort_by", "invalid_filter"],
            "allowed_fields": ["name", "created_at", "status"]
        }
    }
}

4. Duplicate Fields Error:
{
    "duplicate_fields": {
        "message": "Duplicate fields found: name, email",
        "code": "duplicate_fields",
        "details": {
            "fields": ["name", "email"]
        }
    }
}

5. Invalid Filters Error:
{
    "filters": {
        "message": "Invalid filter parameters",
        "code": "invalid_filters",
        "details": {
            "invalid_filters": ["sort_by", "order"],
            "allowed_filters": ["created_at", "status"]
        }
    }
}

6. Combined Multiple Error Types:
{
    "email": {
        "message": "Invalid email format",
        "code": "invalid_email",
        "details": {
            "value": "invalid-email",
            "format": "must be a valid email address"
        }
    },
    "unknown_fields": {
        "message": "Unknown field(s) detected: rating",
        "code": "invalid_fields",
        "details": {
            "fields": ["rating"]
        }
    },
    "duplicate_fields": {
        "message": "Duplicate fields found: name",
        "code": "duplicate_fields",
        "details": {
            "fields": ["name"]
        }
    }
}

7. Integrity Error:
{
    "integrity_error": {
        "message": "User with this email already exists",
        "code": "unique_violation"
    }
}

Key Features:
1. Consistent structure using ErrorResponseDetail class
2. Each error includes message, code, and optional details
3. Supports nested errors for complex validations
4. Handles unknown fields, invalid filters, and duplicate fields
5. Provides both human-readable messages and machine-readable codes
6. Details field can contain additional context specific to each error type
7. All primitive values in details are converted to strings for consistency

Usage Examples:
1. Unknown Fields:
    ErrorResponseDetail(
        message="Unknown field(s) detected: sort_by, rating",
        code="invalid_fields",
        details={
            "fields": ["sort_by", "rating"],
            "allowed_fields": ["name", "created_at"]
        }
    )

2. Invalid Filters:
    ErrorResponseDetail(
        message="Invalid filter parameters",
        code="invalid_filters",
        details={
            "invalid_filters": ["sort_by", "order"],
            "allowed_filters": ["created_at", "status"]
        }
    )

3. Multiple Validation Errors:
    ErrorResponseDetail(
        message="Multiple validation errors",
        code="multiple_errors",
        details={
            "errors": [
                {
                    "message": "Password is too short",
                    "code": "min_length",
                    "min_length": "8"
                },
                {
                    "message": "Password must contain a number",
                    "code": "password_complexity"
                }
            ]
        }
    )
"""


@dataclass
class DrfValidationErrorResponseDetail:
    """
    A class to represent API error response details in a consistent format.

    Attributes:
        message (str): Human-readable error message
        code (str): Machine-readable error code
        details (Dict[str, Any] | None): Additional error context
    """
    message: str
    code: str = "error"
    details: Dict[str, Any] | None = None

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"ErrorResponseDetail(message='{self.message}', code='{self.code}', details={self.details})"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error response detail to a dictionary format.

        Returns:
            Dict[str, Any]: A dictionary containing the error details with the following structure:
            {
                "message": "Human readable message",
                "code": "machine_readable_code",
                "details": {  # Optional
                    "key1": "value1",
                    "key2": "value2"
                }
            }
        """
        result: Dict[str, Any] = {
            'message': self.message,
            'code': self.code
        }
        if self.details is not None:
            if isinstance(self.details, Dict):
                processed_details = {}
                for k, v in self.details.items():
                    if isinstance(v, (str, int, float, bool)):
                        processed_details[k] = str(v)
                    else:
                        processed_details[k] = v
                result['details'] = processed_details
            else:
                result['details'] = str(self.details)
        return result

    @staticmethod
    def convert_error_detail_to_dict(obj: Any) -> Any:
        """
        Convert various error detail types to dictionary format.

        Args:
            obj: The error detail object to convert

        Returns:
            The converted dictionary representation of the error detail
        """
        if isinstance(obj, DrfValidationErrorResponseDetail):
            return obj.to_dict()
        elif isinstance(obj, list):
            return [DrfValidationErrorResponseDetail.convert_error_detail_to_dict(item) for item in obj]
        elif isinstance(obj, Dict):
            if 'unknown_fields' in obj:
                unknown_fields = obj['unknown_fields']
                return {
                    'message': str(unknown_fields['message']),
                    'code': str(unknown_fields['code']),
                    'fields': [str(f) for f in unknown_fields['fields']]
                }
            return {key: DrfValidationErrorResponseDetail.convert_error_detail_to_dict(value) for key, value in obj.items()}
        elif isinstance(obj, DRFErrorDetail):
            return {
                'message': str(obj),
                'code': obj.code if hasattr(obj, 'code') else 'validation_error'
            }
        return obj
