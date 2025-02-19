import json
import re
from typing import Dict, Any, List, Union, Mapping, TypeVar, Generic

from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.fields import ListField, SkipField
from rest_framework.relations import ManyRelatedField
from rest_framework.exceptions import ValidationError

from bodzify_api.validator.AppValidationError import AppValidationError
from bodzify_api.validator.FieldValidationErrorCode import FieldValidationErrorCode

from bodzify_api.utils.validation_error_utils \
    import raise_duplicate_field_error, raise_duplicate_fields_error, \
    raise_unknown_fields_error, raise_unknown_field_error

T = TypeVar('T')


class AppValidationSerializer(serializers.Serializer, Generic[T]):

    REQUEST_FIELD = 'request'

    def _is_list_field(self, field):
        return (
            isinstance(field, (ListField, ManyRelatedField)) or
            getattr(field, 'many', False) or
            getattr(field, 'child', None) is not None
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

    def _check_unknown_fields(
            self,
            initial_data: Dict[str, Any],
            fields: Union[Dict[str, Any], Mapping[str, Any]]) -> List[str]:
        """
        Check for malformed list fields and unknown fields.
        First checks if any list fields are missing the [] suffix,
        then checks for unknown fields.
        """
        # First check for malformed list fields
        for field_name, field in fields.items():
            if self._is_list_field(field) and field_name in initial_data:
                # If it's a list field but used without [] in request, raise error
                error = AppValidationError(
                    field=field_name,
                    message=_(f"List field '{field_name}' must be specified as '{field_name}[]'"),
                    code=FieldValidationErrorCode.MALFORMED_LIST
                )
                self._errors = error.detail
                raise error

        # Then check for unknown fields
        input_fields = set(initial_data.keys())
        known_fields = set()
        for field_name, field in fields.items():
            # Add array notation to list fields in known fields
            if self._is_list_field(field):
                known_fields.add(f"{field_name}[]")
            else:
                known_fields.add(field_name)

        return list(input_fields - known_fields)

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
                code=FieldValidationErrorCode.REQUIRED
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
                                code=FieldValidationErrorCode.UNEXPECTED_LIST
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
            request = self.context.get(self.REQUEST_FIELD)
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
                    value = field.get_value(data)
                    validated_value = field.run_validation(value)
                    validated_data[field.source] = validated_value
                except AppValidationError as exc:
                    raise exc
                except ValidationError as exc:
                    exc_first_detail = str(exc.detail[0] if isinstance(exc.detail, list) else exc.detail)
                    error_code = (
                        FieldValidationErrorCode.REQUIRED
                        if exc_first_detail == "This field is required."
                        else FieldValidationErrorCode.DEFAULT
                    )
                    error = AppValidationError(field=field.field_name,
                                               message=exc_first_detail or 'Invalid input.',
                                               code=error_code)
                    self._errors = error.detail
                    raise error
                except SkipField:
                    continue

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

            self._errors = {}
            self._validated_data = validated_data
            return validated_data

        except AppValidationError as exc:
            self._validated_data = {}
            raise exc
