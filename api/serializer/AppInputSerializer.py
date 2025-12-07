import json
import re
from typing import Any, Generic, TypeVar

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import Field, ListField, SkipField
from rest_framework.relations import ManyRelatedField

from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode


T = TypeVar('T')


class AppInputSerializer(serializers.Serializer, Generic[T]):
    """
    Base serializer class for input validation (POST, PUT, etc.).

    This serializer extends Django REST Framework's Serializer to provide input validation features:
    - Consistent error handling using AppValidationException
    - Multipart form data normalization and validation
    - Duplicate field detection
    - Unknown field detection
    - List field handling with [] suffix for multipart requests

    Note: This serializer is specialized for INPUT validation. Output serializers
    (read-only, for GET responses) do not need AppInputSerializer and can inherit directly
    from serializers.ModelSerializer.

    Key Features:
    ------------
    1. **Error Handling**: Converts all DRF ValidationError exceptions to
       AppValidationException for consistent error responses across the API.

    2. **Multipart Form Data Support**:
       - Normalizes multipart data by extracting single values from lists
       - Enforces [] suffix for list fields in multipart requests
       - Supports both multipart and JSON request formats

    3. **Field Validation**:
       - Detects and rejects duplicate fields (handled by middleware for multipart,
         by serializer for JSON)
       - Detects and rejects unknown fields
       - Properly handles empty sentinel values to skip validation for missing fields

    4. **List Field Handling**:
       - For multipart: List fields MUST use [] suffix (e.g., `artists_names[]`)
       - For JSON: List fields can be specified without [] suffix
       - Automatically maps [] suffix fields to their base field names

    Usage:
    ------
    All INPUT serializers (POST, PUT, etc.) should inherit from AppInputSerializer:

    ```python
    class MyInputSerializer(AppInputSerializer):
        name = AppCharField()
        tags = AppListField(child=AppCharField())
    ```

    Output serializers (read-only) should NOT inherit from AppInputSerializer:
    ```python
    class MyOutputSerializer(serializers.ModelSerializer):
        # Read-only serializer for GET responses
        pass
    ```

    For multipart requests, list fields must use [] suffix:
    - ✅ `tags[]=value1&tags[]=value2` (multipart)
    - ✅ `{"tags": ["value1", "value2"]}` (JSON)

    Error Responses:
    ---------------
    All validation errors are returned as AppValidationException with:
    - field_name: The field that caused the error
    - message: Human-readable error message
    - field_validation_error_code: Machine-readable error code

    See FieldValidationErrorCode for available error codes.
    """

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
        """
        Collect known fields and identify unknown/malformed fields.

        For multipart requests:
        - List fields MUST use [] suffix (e.g., `artists_names[]`)
        - Fields without [] suffix are treated as unknown if they're list fields
        - Automatically maps [] suffix fields to their base field names

        For JSON requests:
        - List fields can be specified without [] suffix
        - Fields with [] suffix are treated as unknown

        Args:
            data: The request data dictionary

        Returns:
            Tuple of (known_fields_set, unknown_fields_list)

        Raises:
            AppValidationException: If a list field in multipart doesn't use [] suffix
        """
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
        """
        Check for duplicate fields in JSON request body.

        Note: For multipart/form-data requests, duplicate field detection is handled
        by DuplicateFieldsMiddleware before the request reaches the serializer.

        This method only checks JSON requests by parsing the raw request body.

        Args:
            request: The request object (must have _raw_body or _request.body)

        Raises:
            AppValidationException: If duplicate fields are found
        """
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
        """
        Validate a single field and convert DRF ValidationError to AppValidationException.

        Handles empty sentinel values by skipping validation for missing fields.
        If a required field is missing, raises AppValidationException with REQUIRED error code.

        Args:
            field: The field to validate
            value: The value to validate

        Returns:
            Validated field value

        Raises:
            AppValidationException: For validation errors with proper error codes
            SkipField: If field is not provided (empty sentinel) and not required
        """
        from rest_framework.fields import empty as empty_sentinel, SkipField
        try:
            # DRF's get_value returns empty sentinel if field not in data
            # If field is required and value is empty_sentinel, raise REQUIRED error
            # Otherwise, skip validation (field not provided and not required)
            if value is empty_sentinel:
                if getattr(field, 'required', False):
                    raise AppValidationException(
                        field_name=field.field_name,
                        message="This field is required.",
                        field_validation_error_code=FieldValidationErrorCode.REQUIRED
                    )
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

        This implementation prevents DRF from converting our custom validation errors
        and adds application-specific validation logic:

        1. Normalizes multipart form data (extracts single values from lists)
        2. Validates known vs unknown fields
        3. Checks for duplicate fields (for JSON requests)
        4. Validates individual fields
        5. Validates the object as a whole

        Args:
            data: The input data to validate (dict for structured data)

        Returns:
            Validated data dictionary

        Raises:
            AppValidationException: For any validation errors with proper error codes
            ImproperlyConfigured: If data is None
        """
        self._initialize_validation_state()

        if data is None:
            raise ImproperlyConfigured('Cannot validate null data')

        try:
            # Handle both flat dictionaries and nested structures
            if isinstance(data, dict):
                request = self.context.get('request')
                is_multipart = request and hasattr(
                    request, 'content_type') and request.content_type and request.content_type.startswith(
                    'multipart/form-data')

                # Check for malformed array fields and unknown fields BEFORE normalization
                # This must happen before normalization so we can detect list fields without [] suffix
                _, unknown_fields = self._collect_known_fields_and_malformed_array_fields_names(data)
                if len(unknown_fields) == 1:
                    raise AppValidationException(field_name=unknown_fields[0],
                                                 message="Unknown field",
                                                 field_validation_error_code=FieldValidationErrorCode.UNKNOWN)
                elif len(unknown_fields) > 1:
                    raise AppValidationException(field_name=", ".join(unknown_fields),
                                                 message="Multiple unknown fields",
                                                 field_validation_error_code=FieldValidationErrorCode.UNKNOWN)

                # Normalize multipart form data: extract single values from lists for non-list fields
                if is_multipart:
                    data = self._normalize_multipart_data(data)
                    # For test client requests, also normalize [''] back to [] for empty list fields
                    # This handles the workaround where AppApiClient converts [] to [''] to preserve empty lists
                    # Note: This is done in the serializer rather than middleware because accessing
                    # request.data in middleware triggers DRF parsing, but overriding it is unreliable
                    # due to DRF's internal caching mechanism
                    if request and request.META.get('HTTP_X_TEST_CLIENT') == 'true':
                        data = self._normalize_test_client_empty_lists(data)

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
            data: The parsed request data dictionary (may be a QueryDict)

        Returns:
            Normalized dictionary with single values extracted from lists
        """
        from django.http import QueryDict

        normalized = {}
        # Use lists() for QueryDict to get all values, items() for regular dict
        if isinstance(data, QueryDict):
            items = data.lists()
        else:
            items = data.items()

        for key, value in items:
            # List fields in multipart use [] suffix - keep them as lists
            if key.endswith('[]'):
                # For QueryDict, value is already a list from lists()
                # For regular dict, ensure it's a list
                if isinstance(data, QueryDict):
                    normalized[key] = value
                else:
                    normalized[key] = value if isinstance(value, list) else [value]
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

    def _normalize_test_client_empty_lists(self, data: dict) -> dict:
        """Normalize [''] back to [] for list fields (with [] suffix) in test client requests.

        AppApiClient converts [] to [''] for list fields to preserve them (DRF's test client
        drops empty lists). This method normalizes [''] back to [] so field validation sees
        empty lists correctly.

        Args:
            data: The normalized multipart data dictionary (may be QueryDict or regular dict)

        Returns:
            Dictionary with [''] converted to [] for list fields
        """
        from django.http import QueryDict

        if isinstance(data, QueryDict):
            result = QueryDict(mutable=True)
            for key, values in data.lists():
                # For list fields (with [] suffix), convert [''] back to []
                if key.endswith('[]') and values == ['']:
                    result.setlist(key, [])
                else:
                    result.setlist(key, values)
            return result
        else:
            # For regular dict, convert [''] to [] for list fields
            normalized = {}
            for key, value in data.items():
                if key.endswith('[]') and isinstance(value, list) and value == ['']:
                    normalized[key] = []
                else:
                    normalized[key] = value
            return normalized
