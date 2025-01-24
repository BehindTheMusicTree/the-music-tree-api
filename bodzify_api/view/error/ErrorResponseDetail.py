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

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ErrorResponseDetail:
    """
    A class to represent API error response details in a consistent format.

    Attributes:
        message (str): Human-readable error message
        code (str): Machine-readable error code
        details (Dict[str, Any] | None): Additional error context
    """
    message: str
    code: str = "error"
    details: Optional[Dict[str, Any]] = None

    @classmethod
    def invalid_uuid(cls, value: str) -> 'ErrorResponseDetail':
        """Create an error detail for invalid UUID values."""
        # Escape curly braces in template variables
        escaped_value = value.replace("{{", "{ {").replace("}}", "} }")
        # Create message without surrounding quotes
        return cls(
            message=f'{escaped_value} is not a valid UUID',
            code="validation_invalid_uuid"
        )

    @classmethod
    def unknown_fields(cls, fields: List[str], allowed_fields: Optional[List[str]] = None) -> 'ErrorResponseDetail':
        """Create an error detail for unknown fields."""
        details = {"fields": fields}
        if allowed_fields is not None:
            details["allowed_fields"] = allowed_fields

        return cls(
            message=f"Unknown field(s) detected: {', '.join(sorted(fields))}",
            code="invalid_fields",
            details=details
        )

    @classmethod
    def duplicate_fields(cls, fields: List[str]) -> 'ErrorResponseDetail':
        """Create an error detail for duplicate fields."""
        return cls(
            message=f"Duplicate fields found: {', '.join(sorted(fields))}",
            code="duplicate_fields",
            details={"fields": fields}
        )

    @classmethod
    def integrity_error(cls, message: str, error_code: str) -> 'ErrorResponseDetail':
        """Create an error detail for integrity errors."""
        return cls(
            message=message,
            code=error_code.lower()
        )

    @classmethod
    def multiple_errors(cls, errors: List[Dict[str, Any]]) -> 'ErrorResponseDetail':
        """Create an error detail for multiple validation errors on a single field."""
        return cls(
            message="Multiple validation errors",
            code="multiple_errors",
            details={"errors": errors}
        )

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
            if isinstance(self.details, dict):
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
