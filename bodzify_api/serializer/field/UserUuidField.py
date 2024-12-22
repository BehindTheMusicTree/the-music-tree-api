
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.request import Request


class UserUuidField(serializers.UUIDField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        uuid = super().to_internal_value(data)
        request = self.context['request']

        if not isinstance(request, Request):  # For linting purposes
            raise ValueError("request must be an Request instance.")

        user = request.user

        if not isinstance(self.queryset, QuerySet):  # For linting purposes
            raise ValueError("queryset must be a QuerySet instance.")

        if not self.queryset.filter(uuid=uuid, user=user).exists():
            raise serializers.ValidationError("Does not exist.")
        return uuid
