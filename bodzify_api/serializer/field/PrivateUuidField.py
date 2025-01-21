
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.request import Request


class PrivateUuidField(serializers.UUIDField):
    def __init__(self, queryset, **kwargs):
        self.queryset = queryset
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if data in [None, ''] and self.allow_null:
            return None

        uuid_value = super().to_internal_value(data)
        request = self.context['request']

        if not isinstance(request, Request):  # For linting purposes
            raise ImproperlyConfigured("request must be a Request instance.")

        user = request.user

        if not isinstance(self.queryset, QuerySet):  # For linting purposes
            raise ImproperlyConfigured("queryset must be a QuerySet instance.")

        try:
            self.queryset.get(uuid=uuid_value, user=user)
            return uuid_value
        except self.queryset.model.DoesNotExist:
            raise serializers.ValidationError("Does not exist.")
