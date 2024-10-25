#!/usr/bin/env python

from rest_framework import serializers


class UserFilteredUUIDField(serializers.UUIDField):
    def __init__(self, queryset, *args, **kwargs):
        self.queryset = queryset
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        uuid = super().to_internal_value(data)
        user = self.context['request'].user
        if not self.queryset.filter(uuid=uuid, user=user).exists():
            raise serializers.ValidationError("Does not exist.")
        return uuid
