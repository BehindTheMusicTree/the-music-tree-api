from typing import Any

from rest_framework.fields import ListField

from api.exception.validation.app.AppValidationException import AppValidationException
from api.exception.validation.FieldValidationErrorCode import FieldValidationErrorCode
from api.serializer.field.AppCharField import AppCharField
from api.serializer.field.AppField import AppField


class ArtistsNamesField(AppField, ListField):
    max_length: int  # Declare max_length as a class variable with type annotation

    def __init__(self, max_length: int, **kwargs):
        # Initialize both parent classes properly
        AppField.__init__(self, **kwargs)
        ListField.__init__(self, child=AppCharField(max_length=max_length), **kwargs)
        self.max_length = max_length  # Keep this for our own validation

    def to_internal_value(self, data: Any) -> list[str] | None:
        if not data:
            return None

        if not isinstance(data, (list, tuple)):
            data = [data]

        for artist_name in data:
            if len(artist_name) > self.max_length:
                self.fail('max_length', max_length=self.max_length)

        unique_artists = set(data)
        if len(unique_artists) < len(data):
            raise AppValidationException(field_name=self.get_error_field_name(),
                                         message='Duplicate artist names are not allowed',
                                         field_validation_error_code=FieldValidationErrorCode.LIST_VALUE_DUPLICATE)

        # Convert tuple to list if necessary to match ListField's expected type
        list_data = list(data) if isinstance(data, tuple) else data
        internal_value = ListField.to_internal_value(self, list_data)
        return internal_value
