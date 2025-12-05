import json
import re
from typing import Any, Generic, TypeVar

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field, ListField, SkipField
from rest_framework.relations import ManyRelatedField

from bodzify_api.exception.validation.app.AppValidationException import AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


T = TypeVar('T')


class AppSerializer(serializers.Serializer, Generic[T]):

    REQUEST_FIELD = 'request'

    def _is_list_field(self, field):
        return (
            isinstance(field, (ListField, ManyRelatedField)) or
            getattr(field, 'many', False) or
            getattr(field, 'child', None) is not None
        )

    @staticmethod
    def _get_raw_field_names(raw_data: str) -> list[str]:
        # Remove whitespace and newlines between tokens to simplify parsing
        raw_data = re.sub(r'\s+', '', raw_data)

        # Find all field names using regex
        # This pattern matches field names in JSON, handling escaped quotes
        pattern = r'"((?:[^"\\]|\\.)*)":'
        matches = re.finditer(pattern, raw_data)

        # Return all field names found in the raw JSON
        return [match.group(1).replace('\\"', '"') for match in matches]

    @classmethod
    def _find_duplicate_fields(cls, raw_data: str) -> list[str]:
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

    def _collect_known_fields_and_malformed_array_fields_names(self, data: dict) -> tuple[set, list]:
        known_fields = set()
        unknown_fields = []
        # Use shallow copy to avoid issues with unpicklable objects like file handles
        updated_data = dict(data)

        # Get request and content type
        request = self.context.get(self.REQUEST_FIELD)
        is_multipart = request and getattr(request, 'content_type', '').startswith('multipart/form-data')

        # First pass: process fields based on content type
        for field_name, field in self.fields.items():
            is_list_field = self._is_list_field(field)
            array_field_name = f"{field_name}[]"

            # Add to known fields (both with and without [] suffix for list fields)
            known_fields.add(field_name)
            if is_list_field:
                known_fields.add(array_field_name)

            # For multipart requests: enforce [] suffix for list fields
            if is_multipart and is_list_field:
                # Error if field is in data without [] suffix
                if field_name in data:
                    raise AppValidationException(
                        field_name=field_name,
                        message=_(f"For multipart requests, list field '{field_name}' must be specified as '{array_field_name}'"),
                        field_validation_error_code=FieldValidationErrorCode.LIST_MALFORMED)

                # Process field with [] suffix if present
                if array_field_name in data:
                    updated_data[field_name] = data[array_field_name]
                    del updated_data[array_field_name]

            # For JSON requests: support fields without [] suffix
            # Any field with [] suffix is just passed through as an unknown field

        # Second pass: collect unknown fields
        for field_name in data.keys():
            # For non-multipart (JSON), we don't recognize fields with [] suffix
            # For multipart, we expect list fields to have [] suffix
            if not is_multipart and field_name.endswith('[]'):
                unknown_fields.append(field_name)
            # For any field without [] suffix or with [] suffix in multipart
            elif field_name not in known_fields:
                unknown_fields.append(field_name)

        return known_fields, unknown_fields

    def _check_duplicate_fields(self, request) -> None:
        if not request:
            return

        raw_body = getattr(request, '_raw_body', None)
        if not raw_body and hasattr(request, '_request'):
            try:
                raw_body = request._request.body
                setattr(request, '_raw_body', raw_body)
            except Exception:
                return

        if raw_body:
            try:
                raw_data = raw_body.decode('utf-8') if isinstance(raw_body, bytes) else str(raw_body)
                duplicates = self._find_duplicate_fields(raw_data)
                if duplicates:
                    if len(duplicates) == 1:
                        raise AppValidationException(field_name=duplicates[0],
                                                     message=_("Duplicate field"),
                                                     field_validation_error_code=FieldValidationErrorCode.DUPLICATE)
                    raise AppValidationException(field_name=f", ".join(duplicates),
                                                 message=_("Multiple duplicate fields"),
                                                 field_validation_error_code=FieldValidationErrorCode.DUPLICATE)
            except (UnicodeDecodeError, AttributeError):
                pass

    def _validate_field(self, field: Field, value) -> Any:
        from rest_framework.fields import empty as empty_sentinel, SkipField
        try:
            # DRF's get_value returns empty sentinel if field not in data
            # SkipField should be raised by get_value, but if we get empty sentinel,
            # we should skip validation (field not provided)
            if value is empty_sentinel:
                raise SkipField()
            return field.run_validation(value)
        except AppValidationException as exc:
            raise exc
        except SkipField:
            raise
        except ValidationError as exc:
            try:
                detail = exc.detail
                exc_first_detail = str(detail[0] if isinstance(detail, list) else detail)
            except (AttributeError, TypeError):
                try:
                    exc_first_detail = str(exc)
                except Exception:
                    exc_first_detail = 'Invalid input.'
            error_code = (FieldValidationErrorCode.REQUIRED
                          if exc_first_detail == "This field is required."
                          else FieldValidationErrorCode.DEFAULT)
            error = AppValidationException(field_name=field.field_name,
                                           message=exc_first_detail or 'Invalid input.',
                                           field_validation_error_code=error_code)
            try:
                self._errors = error.detail
            except (AttributeError, TypeError):
                self._errors = error.errors
            raise error

    def _validate_object(self, validated_data: dict) -> dict:
        try:
            return self.validate(validated_data)
        except AppValidationException as exc:
            try:
                self._errors = exc.detail
            except (AttributeError, TypeError):
                self._errors = exc.errors
            raise
        except ValidationError as exc:
            try:
                detail = exc.detail
                detail_str = str(detail[0] if isinstance(detail, list) else detail)
            except (AttributeError, TypeError):
                try:
                    detail_str = str(exc)
                except Exception:
                    detail_str = 'Invalid input.'
            error = AppValidationException(message=detail_str,
                                           field_validation_error_code=FieldValidationErrorCode.DEFAULT)
            try:
                self._errors = error.detail
            except (AttributeError, TypeError):
                self._errors = error.errors
            raise error

    def _initialize_validation_state(self):
        if not hasattr(self, '_validated_data'):
            self._validated_data = {}
        if not hasattr(self, '_errors'):
            self._errors = {}

    def _validate_fields(self, data: dict) -> dict:
        validated_data = {}
        for field in self._writable_fields:
            try:
                value = field.get_value(data)
                validated_value = self._validate_field(field, value)
                validated_data[field.source] = validated_value
            except AppValidationException:
                raise
            except SkipField:
                continue
        return validated_data

    def run_validation(self, data):
        """
        Override run_validation to handle field validation and preserve AppValidationError.
        This implementation prevents DRF from converting our custom validation errors.
        """
        self._initialize_validation_state()

        if data is None:
            raise ImproperlyConfigured('Cannot validate null data')

        try:
            # Handle both flat dictionaries and nested structures
            if isinstance(data, dict):
                # Normalize multipart form data: extract single values from lists for non-list fields
                request = self.context.get('request')
                if request and hasattr(
                        request, 'content_type') and request.content_type and request.content_type.startswith(
                        'multipart/form-data'):
                    data = self._normalize_multipart_data(data)

                # Get known fields and check for unknown fields
                _, unknown_fields = self._collect_known_fields_and_malformed_array_fields_names(data)
                if len(unknown_fields) == 1:
                    raise AppValidationException(field_name=unknown_fields[0],
                                                 message="Unknown field",
                                                 field_validation_error_code=FieldValidationErrorCode.UNKNOWN)
                elif len(unknown_fields) > 1:
                    raise AppValidationException(field_name=", ".join(unknown_fields),
                                                 message="Multiple unknown fields",
                                                 field_validation_error_code=FieldValidationErrorCode.UNKNOWN)

                self._check_duplicate_fields(self.context.get(self.REQUEST_FIELD))

                # Use the properly transformed data from _collect_known_fields_and_malformed_array_fields_names
                updated_data = dict(data)  # Create a copy to avoid modifying the input
                field_name_mapping = {}  # Keep track of original field names
                for field_name, field in self.fields.items():
                    if self._is_list_field(field) and f"{field_name}[]" in updated_data:
                        field_name_mapping[field_name] = f"{field_name}[]"
                        updated_data[field_name] = updated_data.pop(f"{field_name}[]")

                try:
                    validated_data = self._validate_fields(updated_data)
                    validated_data = self._validate_object(validated_data)
                except AppValidationException as e:
                    # Map back to original field name if it was transformed
                    if e.field in field_name_mapping:
                        e.errors = {field_name_mapping[e.field]: e.errors[e.field]}
                        e.field = field_name_mapping[e.field]
                    raise e
            else:
                # For non-dict data, let the serializer's to_internal_value handle it
                validated_data = self.to_internal_value(data)

            self._errors = {}
            self._validated_data = validated_data
            return validated_data
        except (KeyError, TypeError) as e:
            raise AppValidationException(field_name=str(e),
                                         message=str(e),
                                         field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID)
        except AppValidationException as e:
            raise e
        except ValidationError as e:
            raise AppValidationException(field_name=str(e),
                                         message=str(e),
                                         field_validation_error_code=FieldValidationErrorCode.FORMAT_INVALID)

    def _normalize_multipart_data(self, data: dict) -> dict:
        """
        Normalize multipart form data by extracting single values from lists
        for non-list fields. List fields are identified by the [] suffix.

        Args:
            data: The parsed request data dictionary

        Returns:
            Normalized dictionary with single values extracted from lists
        """
        normalized = {}
        for key, value in data.items():
            # List fields in multipart use [] suffix - keep them as lists
            if key.endswith('[]'):
                normalized[key] = value
            # For non-list fields, extract single value from list if present
            elif isinstance(value, list):
                if len(value) == 0:
                    normalized[key] = None
                elif len(value) == 1:
                    normalized[key] = value[0]
                else:
                    # Multiple values for non-list field - keep as list
                    # (this shouldn't happen for single-value fields, but handle gracefully)
                    normalized[key] = value
            else:
                normalized[key] = value
        return normalized
