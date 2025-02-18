import json
import re
from typing import Dict, Any, List, Union, Mapping, Optional, TypeVar, Generic

from django.db import models
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.fields import CharField, ListField, Field
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode

from bodzify_api.utils.validation_error_utils \
    import raise_duplicate_field_error, raise_duplicate_fields_error, \
    raise_unknown_fields_error, raise_unknown_field_error

T = TypeVar('T')


class AppValidationSerializer(serializers.Serializer, Generic[T]):
    """Base serializer class that provides common validation functionality."""

    def _is_list_field(self, field):
        """Check if a field is designed to accept list values."""
        return (
            isinstance(field, (ListField, ManyRelatedField)) or
            getattr(field, 'many', False) or
            getattr(field, 'child', None) is not None
        )

    def run_validation(self, data):
        """
        Override run_validation to handle field validation and preserve AppValidationError.
        This implementation prevents DRF from converting our custom validation errors.
        """
        if not hasattr(self, '_validated_data'):
            self._validated_data = {}
        if not hasattr(self, '_errors'):
            self._errors = {}

        if data is None:
            error = AppValidationError(
                message="This field is required.",
                code=FieldValidationErrorCode.DEFAULT
            )
            self._errors = error.detail
            raise error

        try:
            # Run field validations
            if isinstance(data, dict):
                # 1. Validate field types (list values)
                for field_name, field in self.fields.items():
                    if field_name in data:
                        value = data[field_name]
                        if isinstance(value, list) and not self._is_list_field(field):
                            error = AppValidationError(
                                field=field_name,
                                message=_("The field does not accept list values"),
                                code=FieldValidationErrorCode.UNEXPECTED_LIST_VALUE
                            )
                            self._errors = error.detail
                            raise error

                # 2. Check for unknown fields
                unknown_keys = self._check_unknown_fields(data, self.fields)
                if len(unknown_keys) == 1:
                    raise_unknown_field_error(unknown_keys[0])
                elif len(unknown_keys) > 1:
                    raise_unknown_fields_error(unknown_keys)

            # 3. Check for duplicate fields
            request = self.context.get('request')
            if request:
                raw_body = getattr(request, '_raw_body', None)
                if not raw_body and hasattr(request, '_request'):
                    try:
                        raw_body = request._request.body
                        setattr(request, '_raw_body', raw_body)
                    except Exception:
                        pass

                if raw_body:
                    try:
                        raw_data = raw_body.decode('utf-8') if isinstance(raw_body, bytes) else str(raw_body)
                        duplicates = self._find_duplicate_fields(raw_data)
                        if duplicates:
                            if len(duplicates) == 1:
                                raise_duplicate_field_error(duplicates[0])
                            raise_duplicate_fields_error(duplicates)
                    except (UnicodeDecodeError, AttributeError):
                        pass

            # 4. Run field-level validation
            validated_data = {}
            for field in self._writable_fields:
                try:
                    validated_value = field.run_validation(field.get_value(data))
                    if validated_value is not None:
                        validated_data[field.source] = validated_value
                except AppValidationError as exc:
                    self._errors = exc.detail
                    raise
                except ValidationError as exc:
                    # Ensure we have a valid field name
                    kwargs = {
                        'message': str(exc.detail[0] if isinstance(exc.detail, list) else exc.detail),
                        'code': FieldValidationErrorCode.DEFAULT
                    }
                    if field.field_name:
                        kwargs['field'] = field.field_name
                    error = AppValidationError(**kwargs)
                    self._errors = error.detail
                    raise error

            # 5. Run object-level validation
            try:
                validated_data = self.validate(validated_data)
            except AppValidationError as exc:
                self._errors = exc.detail
                raise
            except ValidationError as exc:
                error = AppValidationError(
                    message=str(exc.detail[0] if isinstance(exc.detail, list) else exc.detail),
                    code=FieldValidationErrorCode.DEFAULT
                )
                self._errors = error.detail
                raise error

            # Success path
            self._errors = {}
            self._validated_data = validated_data
            return validated_data

        except AppValidationError:
            self._validated_data = {}
            raise

    @staticmethod
    def _get_raw_field_names(raw_data: str) -> List[str]:
        """Extract field names from raw JSON data."""
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
        """Check for unknown fields in the input data."""
        return list(set(initial_data.keys()) - set(fields.keys()))

    @classmethod
    def _find_duplicate_fields(cls, raw_data: str) -> List[str]:
        """Find duplicate field names in raw JSON data."""
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
