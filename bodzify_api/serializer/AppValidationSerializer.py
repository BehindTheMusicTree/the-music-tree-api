import json
import re
from typing import Dict, Any, List, Union, Mapping

from rest_framework import serializers
from rest_framework.fields import CharField, ListField
from rest_framework.relations import ManyRelatedField
from rest_framework.exceptions import ValidationError

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode

from bodzify_api.utils.validation_error_utils \
    import raise_duplicate_field_error, raise_duplicate_fields_error, \
    raise_unknown_fields_error, raise_unknown_field_error


class AppValidationSerializer(serializers.Serializer):
    """Base serializer class that provides common validation functionality."""

    def _is_list_field(self, field):
        """Check if a field is designed to accept list values."""
        return (
            isinstance(field, (ListField, ManyRelatedField)) or
            getattr(field, 'many', False) or
            getattr(field, 'child', None) is not None
        )

    def run_validation(self, data):
        """Override run_validation to preserve AppValidationError through the validation chain."""
        # First check for list values in non-list fields
        if isinstance(data, dict):
            for field_name, field in self.fields.items():
                if field_name in data:
                    value = data[field_name]
                    if isinstance(value, list) and not self._is_list_field(field):
                        raise AppValidationError.from_filterset(
                            field=field_name,
                            message=f"The field does not accept list values",
                            code=FieldValidationErrorCode.UNEXPECTED_LIST_VALUE
                        )

        # Run parent validation but preserve our exception
        try:
            return super().run_validation(data)
        except ValidationError as e:
            # If it's already our custom error, re-raise it
            if isinstance(e, AppValidationError):
                raise
            # For DRF validation errors, wrap them in our format
            raise AppValidationError.from_field(
                field='non_field_errors',
                message=str(e.detail if hasattr(e, 'detail') else e),
                code=FieldValidationErrorCode.INVALID_FORMAT
            )

    @staticmethod
    def _get_raw_field_names(raw_data: str) -> List[str]:
        # Remove whitespace and newlines between tokens to simplify parsing
        raw_data = re.sub(r'\s+', '', raw_data)

        # Find all field names using regex
        # This pattern matches field names in JSON, handling escaped quotes
        pattern = r'"((?:[^"\\]|\\.)*)":'
        matches = re.finditer(pattern, raw_data)

        # Return all field names found in the raw JSON
        return [match.group(1).replace('\\"', '"') for match in matches]

    @staticmethod
    def _check_unknown_fields(
            initial_data: Dict[str, Any],
            fields: Union[Dict[str, Any],
                          Mapping[str, Any]]) -> List[str]:

        return list(set(initial_data.keys()) - set(fields.keys()))

    @classmethod
    def _find_duplicate_fields(cls, raw_data: str) -> List[str]:
        try:
            field_names = cls._get_raw_field_names(raw_data)
            field_counts = {}
            duplicates = []

            for field in field_names:
                if field in field_counts:
                    if field_counts[field] == 1:  # Only add to duplicates once
                        duplicates.append(field)
                    field_counts[field] += 1
                else:
                    field_counts[field] = 1

            return duplicates
        except (UnicodeDecodeError, AttributeError, json.JSONDecodeError):
            return []

    def _validate_fields(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        # Check for unknown fields
        if hasattr(self, 'initial_data') and hasattr(self, 'fields'):
            unknown_keys = self._check_unknown_fields(self.initial_data, self.fields)
            if len(unknown_keys) == 1:
                raise_unknown_field_error(unknown_keys[0])
            elif len(unknown_keys) > 1:
                raise_unknown_fields_error(unknown_keys)

        # Check for duplicate fields
        request = self.context.get('request')
        if request:
            # Try to get raw body from different possible locations
            raw_body = getattr(request, '_raw_body', None)

            # If we don't have the raw body stored, try to get it from the request
            # and store it before it's consumed
            if not raw_body and hasattr(request, '_request'):
                try:
                    raw_body = request._request.body
                    # Store the raw body for future access
                    setattr(request, '_raw_body', raw_body)
                except Exception:
                    # If we can't access the body, it might have been consumed
                    pass

            if raw_body:
                try:
                    # Convert bytes to string if needed
                    if isinstance(raw_body, bytes):
                        raw_data = raw_body.decode('utf-8')
                    else:
                        raw_data = str(raw_body)

                    duplicates = self._find_duplicate_fields(raw_data)
                    if duplicates:
                        if len(duplicates) == 1:
                            raise_duplicate_field_error(duplicates[0])

                        raise_duplicate_fields_error(duplicates)
                except (UnicodeDecodeError, AttributeError):
                    pass

        return attrs

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the input data."""
        attrs = self._validate_fields(attrs)
        return super().validate(attrs)
