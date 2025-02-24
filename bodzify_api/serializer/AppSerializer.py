import json
import re
from typing import Any, Dict, List, TypeVar, Generic

from django.utils.translation import gettext as _
from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from rest_framework.fields import Field, ListField, SkipField
from rest_framework.relations import ManyRelatedField
from rest_framework.exceptions import ValidationError

from bodzify_api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from bodzify_api.exception.validation.app.AppValidationError import AppValidationError

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
    def _get_raw_field_names(raw_data: str) -> List[str]:
        # Remove whitespace and newlines between tokens to simplify parsing
        raw_data = re.sub(r'\s+', '', raw_data)

        # Find all field names using regex
        # This pattern matches field names in JSON, handling escaped quotes
        pattern = r'"((?:[^"\\]|\\.)*)":'
        matches = re.finditer(pattern, raw_data)

        # Return all field names found in the raw JSON
        return [match.group(1).replace('\\"', '"') for match in matches]

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

    def _validate_field_format(self, field_name: str, field, data: Dict) -> None:
        if self._is_list_field(field):
            if field_name in data:
                raise AppValidationError(
                    field_name=field_name,
                    message=_(f"List field '{field_name}' must be specified as '{field_name}[]'"),
                    field_validation_error_code=FieldValidationErrorCode.MALFORMED_LIST
                )
        elif field_name in data and isinstance(data[field_name], list):
            raise AppValidationError(
                field_name=field_name,
                message=_("The field does not accept list values"),
                field_validation_error_code=FieldValidationErrorCode.UNEXPECTED_LIST
            )

    def _collect_known_fields_and_malformed_array_fields_names(self, data: Dict) -> tuple[set, list]:
        known_fields = set()
        unknown_fields = []
        updated_data = data.copy()

        # First pass: check for malformed arrays and build known fields
        for field_name, field in self.fields.items():
            is_list_field = self._is_list_field(field)
            array_field_name = f"{field_name}[]"

            # Check if field exists in data but missing [] suffix
            if field_name in data and is_list_field:
                raise AppValidationError(
                    field_name=field_name,
                    message=_(f"List field '{field_name}' must be specified as '{array_field_name}'"),
                    field_validation_error_code=FieldValidationErrorCode.MALFORMED_LIST
                )

            # Add to known fields without [] suffix
            known_fields.add(field_name)

            # If it's a list field and has [] suffix in data, update the data to remove []
            if is_list_field and array_field_name in data:
                updated_data[field_name] = data[array_field_name]
                del updated_data[array_field_name]

        # Second pass: collect unknown fields from updated data
        for field_name in data.keys():
            base_field_name = field_name[:-2] if field_name.endswith('[]') else field_name
            if base_field_name not in known_fields:
                unknown_fields.append(field_name)

        return known_fields, unknown_fields

    def _collect_list_field_values(self, field_name: str | None, data: Dict) -> Any:
        """
        Collects values for list fields, handling both array notation and direct values.
        Args:
            field_name: The name of the field without [] suffix
            data: The data dictionary containing the field values
        Returns:
            The field value or None if not found
        """
        if field_name is None:
            return None

        array_field_name = f"{field_name}[]"
        if array_field_name in data:
            return data[array_field_name]
        return data.get(field_name)

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
                        raise AppValidationError(
                            field_name=duplicates[0],
                            message=_("Duplicate field"),
                            field_validation_error_code=FieldValidationErrorCode.FIELD_DUPLICATE
                        )
                    raise AppValidationError(
                        field_name=f", ".join(duplicates),
                        message=_("Multiple duplicate fields"),
                        field_validation_error_code=FieldValidationErrorCode.FIELD_DUPLICATE)
            except (UnicodeDecodeError, AttributeError):
                pass

    def _validate_field(self, field: Field, value) -> Any:
        try:
            return field.run_validation(value)
        except AppValidationError as exc:
            raise exc
        except ValidationError as exc:
            exc_first_detail = str(exc.detail[0] if isinstance(exc.detail, list) else exc.detail)
            error_code = (
                FieldValidationErrorCode.REQUIRED
                if exc_first_detail == "This field is required."
                else FieldValidationErrorCode.DEFAULT
            )
            error = AppValidationError(
                field_name=field.field_name,
                message=exc_first_detail or 'Invalid input.',
                field_validation_error_code=error_code
            )
            self._errors = error.detail
            raise error

    def _validate_object(self, validated_data: Dict) -> Dict:
        try:
            return self.validate(validated_data)
        except AppValidationError as exc:
            self._errors = exc.detail
            raise
        except ValidationError as exc:
            error = AppValidationError(
                message=str(exc.detail[0] if isinstance(exc.detail, list) else exc.detail),
                field_validation_error_code=FieldValidationErrorCode.DEFAULT
            )
            self._errors = error.detail
            raise error

    def _initialize_validation_state(self):
        if not hasattr(self, '_validated_data'):
            self._validated_data = {}
        if not hasattr(self, '_errors'):
            self._errors = {}

    def _validate_fields(self, data: Dict) -> Dict:
        validated_data = {}
        for field in self._writable_fields:
            try:
                value = field.get_value(data)
                validated_value = self._validate_field(field, value)
                validated_data[field.source] = validated_value
            except AppValidationError:
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
            if not isinstance(data, Dict):
                raise ImproperlyConfigured('Data must be a dictionary')

            _, unknown_fields = self._collect_known_fields_and_malformed_array_fields_names(data)
            if len(unknown_fields) == 1:
                raise AppValidationError(
                    field_name=unknown_fields[0],
                    message="Unknown field",
                    field_validation_error_code=FieldValidationErrorCode.UNKNOWN_FIELD
                )
            elif len(unknown_fields) > 1:
                raise AppValidationError(
                    field_name=", ".join(unknown_fields),
                    message="Multiple unknown fields",
                    field_validation_error_code=FieldValidationErrorCode.UNKNOWN_FIELD
                )

            self._check_duplicate_fields(self.context.get(self.REQUEST_FIELD))

            data_without_array_suffixe = {key[:-2] if key.endswith('[]') else key: value for key, value in data.items()}
            validated_data = self._validate_fields(data_without_array_suffixe)

            validated_data = self._validate_object(validated_data)

            self._errors = {}
            self._validated_data = validated_data
            return validated_data

        except AppValidationError as exc:
            self._validated_data = {}
            raise exc
