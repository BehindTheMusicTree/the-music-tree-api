
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.request import Request


class NullablePrivateUuidField(serializers.UUIDField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        # Set allow_null=True by default unless explicitly overridden
        if 'allow_null' not in kwargs:
            kwargs['allow_null'] = True
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if data in [None, ''] and self.allow_null:
            return None

        uuid = super().to_internal_value(data)
        request = self.context['request']

        if not isinstance(request, Request):  # For linting purposes
            raise ImproperlyConfigured("request must be a Request instance.")

        user = request.user

        if not isinstance(self.queryset, QuerySet):  # For linting purposes
            raise ImproperlyConfigured("queryset must be a QuerySet instance.")

        try:
            return self.queryset.get(uuid=uuid, user=user)
        except self.queryset.model.DoesNotExist:
            raise serializers.ValidationError("Does not exist.")
