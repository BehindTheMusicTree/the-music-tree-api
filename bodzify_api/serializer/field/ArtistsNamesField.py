from typing import Any

from rest_framework import serializers
from rest_framework.fields import ListField

from bodzify_api.exception.validation.app.AppValidationError import \
    AppValidationException
from bodzify_api.exception.validation.FieldValidationErrorCode import \
    FieldValidationErrorCode
from bodzify_api.serializer.field.AppField import AppField


class ArtistsNamesField(AppField, ListField):
    max_length: int  # Declare max_length as a class variable with type annotation

    def __init__(self, max_length: int, **kwargs):
        # Initialize both parent classes properly
        AppField.__init__(self, **kwargs)
        ListField.__init__(self, child=serializers.CharField(max_length=max_length), **kwargs)
        self.max_length = max_length  # Keep this for our own validation

    def to_internal_value(self, data: Any) -> list[str] | None:
        if not data:
            return None

        if isinstance(data, (list, tuple)):
            if '' in data or None in data:
                raise AppValidationException(
                    field_name=self.get_error_field_name(),
                    message='Empty artist names are not allowed when another value is specified',
                    field_validation_error_code=FieldValidationErrorCode.ARTIST_NAME_EMPTY_IN_LIST
                )
        else:
            data = [data]

        for artist_name in data:
            if len(artist_name) > self.max_length:
                self.fail('max_length', max_length=self.max_length)

        unique_artists = set(data)
        if len(unique_artists) < len(data):
            raise AppValidationException(
                field_name=self.get_error_field_name(),
                message='Duplicate artist names are not allowed',
                field_validation_error_code=FieldValidationErrorCode.ARTIST_NAMES_DUPLICATE
            )

        # Convert tuple to list if necessary to match ListField's expected type
        list_data = list(data) if isinstance(data, tuple) else data
        internal_value = ListField.to_internal_value(self, list_data)
        return internal_value
