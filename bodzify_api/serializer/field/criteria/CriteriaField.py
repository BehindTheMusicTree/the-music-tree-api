from typing import Any

from django.db.models.query import QuerySet
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
    """

    def __init__(
            self, input_types: list[CriteriaFieldInputType], queryset: QuerySet = Criteria.objects.all(), **kwargs):
        self.input_types = input_types
        self._allow_blank = kwargs.get('allow_blank', True)
        self._allow_null = kwargs.get('allow_null', True)

        super().__init__(queryset=queryset, **kwargs)

        # Create validation fields based on enabled input types
        self.char_field = None
        if CriteriaFieldInputType.NAME in input_types:
            self.char_field = AppCharField(
                required=self.required,
                max_length=settings.CRITERIA_NAME_LEN_MAX,
                allow_blank=self._allow_blank,
                allow_null=self._allow_null
            )

        # Initialize UUID validation if enabled
        self.uuid_field = None
        if CriteriaFieldInputType.UUID in input_types:
            self.uuid_field = PrivateUuidField(queryset=queryset, allow_null=self._allow_null)

    def bind(self, field_name: str, parent: Any) -> None:
        """
        Called when the field is bound to a serializer.
        Propagate the field name to child fields for proper error reporting.
        """
        super().bind(field_name, parent)
        if self.char_field:
            self.char_field.bind(field_name, parent)
        if self.uuid_field:
            self.uuid_field.bind(field_name, parent)

    def to_internal_value(self, data: Any) -> Any:
        if data in [None, '']:
            if not self._allow_null:
                self.fail('null')
            return None

        # Check if input looks like a UUID (basic format check)
        looks_like_uuid = isinstance(data, str) and len(data.split('-')) == 5

        # If it looks like a UUID and UUID input is enabled
        if looks_like_uuid:
            if CriteriaFieldInputType.UUID in self.input_types and self.uuid_field is not None:
                return self.uuid_field.to_internal_value(data)
            else:
                self.fail('invalid', detail='UUID input type is not enabled for this field.')

        # If it doesn't look like a UUID, try name validation
        if CriteriaFieldInputType.NAME in self.input_types and self.char_field:
            validated_name = self.char_field.to_internal_value(data)
            model_class = self.get_queryset().model
            user = self.context['request'].user
            return model_class.objects.get_or_create(user=user, name=validated_name)[0]

        self.fail('invalid', detail='Field must be a valid UUID or name.')

    def to_representation(self, value: Any) -> str:
        return str(value.uuid)
