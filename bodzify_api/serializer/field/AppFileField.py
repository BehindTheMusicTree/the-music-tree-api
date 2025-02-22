
from rest_framework import serializers

from bodzify_api.serializer.field.AppField import AppField


class AppFileField(AppField, serializers.FileField):

    def __init__(self, *args, **kwargs):
        self.field_name = kwargs.pop('field_name', None)
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        return serializers.FileField.to_internal_value(self, data)
