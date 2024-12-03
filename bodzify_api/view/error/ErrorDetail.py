from dataclasses import dataclass
from typing import Any, Dict, Union
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.exceptions import ErrorDetail as DRFErrorDetail


@dataclass
class ErrorDetail:
    """Custom error detail class for API responses."""
    message: str
    code: str = "error"
    details: Union[Dict[str, Any], None] = None

    @classmethod
    def invalid_uuid(cls, value: str) -> 'ErrorDetail':
        """Create an error detail for invalid UUID."""
        # Escape curly braces in template variables
        escaped_value = value.replace("{{", "{ {").replace("}}", "} }")
        # Create message without surrounding quotes
        return cls(
            message=f'{escaped_value} is not a valid UUID',
            code="validation_invalid_uuid"
        )

    def __str__(self) -> str:
        """String representation of the error detail."""
        return self.message

    def __repr__(self) -> str:
        """Detailed string representation of the error detail."""
        return f"ErrorDetail(message='{self.message}', code='{self.code}', details={self.details})"

    def to_dict(self) -> Dict[str, Any]:
        """Convert the error detail to a dictionary."""
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

    def to_drf_error_detail(self) -> DRFErrorDetail:
        """Convert to DRF's ErrorDetail for compatibility."""
        error = DRFErrorDetail(str(self.message))
        error.code = self.code
        return error