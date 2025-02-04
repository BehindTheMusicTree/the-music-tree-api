
from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.request import Request

from bodzify_api.utils.validation_error_utils import raise_validation_error
from bodzify_api.view.error.FieldValidationErrorCode import FieldValidationErrorCode


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
            field_name = self.field_name if self.field_name is not None else 'uuid_field'
            raise_validation_error(
                message='Resource does not exist for this user',
                field_validation_error_code=FieldValidationErrorCode.FIELD_RESOURCE_NOT_OWNED,
                field=field_name
            )
