from typing import Any, Optional
from rest_framework.fields import Field


class AppField(Field):
    """
    Base field class for all app-specific serializer fields.
    Provides consistent error field name handling.
    """

    def get_error_field_name(self) -> Optional[str]:
        if hasattr(self, 'field_name') and self.field_name:
            return self.field_name
        return None

    def to_internal_value(self, data: Any) -> Any:
        """
        To prevent suclasses' calls to super().to_internal_value() from raising NotImplementedError.
        """
        return None
