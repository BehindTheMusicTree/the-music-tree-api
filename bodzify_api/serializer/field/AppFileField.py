
from rest_framework import serializers

from bodzify_api.serializer.field.AppField import AppField


class AppFileField(AppField, serializers.FileField):

    def to_internal_value(self, data):
        return serializers.FileField.to_internal_value(self, data)
