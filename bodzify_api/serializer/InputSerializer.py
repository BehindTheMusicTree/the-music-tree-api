#!/usr/bin/env python

from django.forms import ValidationError
from rest_framework import serializers


class InputSerializer(serializers.Serializer):

    def validate(self, data):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())  # type: ignore
            if unknown_keys:
                raise ValidationError("Unknown fields: {}".format(unknown_keys))
        return data
