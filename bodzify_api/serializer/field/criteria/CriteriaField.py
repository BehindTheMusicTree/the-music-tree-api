from typing import Any

from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from bodzify_api import settings
from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.field.AppField import AppField
from bodzify_api.serializer.field.criteria.CriteriaFieldInputType import CriteriaFieldInputType
from bodzify_api.serializer.field.foreign_key.PrivateUuidField import PrivateUuidField


class CriteriaField(AppField, PrimaryKeyRelatedField):
    """
    A unified field that handles both UUID and name-based criteria inputs.
    Automatically detects input type and processes accordingly.
    Can be used directly or inherited by specific criteria type fields.
    """

    def __init__(
            self, input_types: list[CriteriaFieldInputType], queryset: QuerySet = Criteria.objects.all(), **kwargs):
        self.input_types = input_types
        self._allow_blank = kwargs.get('allow_blank', True)
        self._allow_null = kwargs.get('allow_null', True)

        # Initialize base classes first
        super().__init__(queryset=queryset, **kwargs)

        # Create validation fields based on enabled input types
        self.char_field = None
        if CriteriaFieldInputType.NAME in input_types:
            char_kwargs = {
                'max_length': settings.CRITERIA_NAME_LEN_MAX,
                'allow_blank': self._allow_blank,
                'allow_null': self._allow_null
            }
            self.char_field = AppCharField(**char_kwargs)

        # Initialize UUID validation if enabled
        self._uuid_validator = None
        if CriteriaFieldInputType.UUID in input_types:
            self._uuid_validator = PrivateUuidField(queryset=queryset, allow_null=self._allow_null)

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        request = self.context.get('request')
        if request and request.user:
            return queryset.filter(user=request.user)
        return queryset

    def to_internal_value(self, data: Any) -> Any:
        if data in [None, '']:
            if not self._allow_null:
                self.fail('null')
            return None

        # Try UUID first if enabled
        if CriteriaFieldInputType.UUID in self.input_types and self._uuid_validator:
            try:
                return self._uuid_validator.to_internal_value(data)
            except ValidationError:
                pass  # Not a valid UUID or not found, try next input type

        # Try name if enabled
        if CriteriaFieldInputType.NAME in self.input_types and self.char_field:
            try:
                validated_name = self.char_field.to_internal_value(data)
                return self.get_queryset().get_or_create(name=validated_name)[0]
            except ValidationError as e:
                self.fail('invalid', detail=str(e))
            except Exception as e:
                raise ValidationError(f"Error processing criteria name: {str(e)}")

        self.fail('invalid', detail='Invalid criteria input')

    def to_representation(self, value: Any) -> str:
        return str(value.uuid)
