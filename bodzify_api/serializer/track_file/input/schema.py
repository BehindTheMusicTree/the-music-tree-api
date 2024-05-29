#!/usr/bin/env python

import binascii
from rest_framework import serializers

from bodzify_api.model.TrackFile import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL, TrackFile


class FIELDS:
    FILE = ATTRIBUTES_LABEL.FILE
    FINGERPRINT_CHAR = ATTRIBUTES_LABEL.FINGERPRINT
    SHOULD_CHECK_IF_FINGERPRINT_EXISTS = "should_check_if_fingerprint_exists"


class TrackFileSchemaSerialazer(serializers.Serializer):
    file = serializers.FileField()

    # Django serializers don't support binary fields. We pass the fingerprint as a string and convert it to binary
    # creating the instance of the model.
    fingerprint = serializers.CharField(required=False)
    should_check_if_fingerprint_exists = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if FIELDS.FINGERPRINT_CHAR in attrs:
            if FIELDS.SHOULD_CHECK_IF_FINGERPRINT_EXISTS in attrs and attrs[
                    FIELDS.SHOULD_CHECK_IF_FINGERPRINT_EXISTS]:
                fingerprint = binascii.unhexlify(attrs[FIELDS.FINGERPRINT_CHAR])
                if TrackFile.objects.filter(fingerprint=fingerprint).exists():
                    raise serializers.ValidationError(
                        "This track already exists in the library (acoustic fingerprint check).")

        return super().validate(attrs)
