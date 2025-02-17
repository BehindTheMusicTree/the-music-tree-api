from rest_framework.fields import Field


class AppField(Field):
    """
    Base field class for all app-specific serializer fields.
    Provides consistent error field name handling.
    """
    
    def get_error_field_name(self) -> str:
        """
        Get the field name for error reporting.
        Used by AppValidationError to ensure consistent field names in error messages.
        
        Returns:
            The field name if set, otherwise the lowercase class name
        """
        if hasattr(self, 'field_name') and self.field_name:
            return self.field_name
        return self.__class__.__name__.lower()