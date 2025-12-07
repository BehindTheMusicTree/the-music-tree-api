from django.db import models
from rest_framework import serializers


class AppOneToOneField(models.OneToOneField):
    def __init__(self, to, **kwargs):
        super().__init__(to, **kwargs)
        self.serializer_field_class = serializers.UUIDField