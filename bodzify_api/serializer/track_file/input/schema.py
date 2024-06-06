#!/usr/bin/env python

import binascii
from rest_framework import serializers

from bodzify_api.model.TrackFile import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL, TrackFile


class FIELDS:
    FILE = ATTRIBUTES_LABEL.FILE
    FINGERPRINT_CHAR = ATTRIBUTES_LABEL.FINGERPRINT
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = "should_cancel_if_duplicate_fingerprint"


class TrackFileSchemaSerialazer(serializers.Serializer):
    file = serializers.FileField()

    # Django serializers don't support binary fields. We pass the fingerprint as a string and convert it to binary
    # creating the instance of the model.
    fingerprint = serializers.CharField(required=False)
    should_cancel_if_duplicate_fingerprint = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if FIELDS.FINGERPRINT_CHAR in attrs:
            if FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT in attrs and attrs[
                    FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT]:
                fingerprint = binascii.unhexlify(attrs[FIELDS.FINGERPRINT_CHAR])
                if TrackFile.objects.filter(fingerprint=fingerprint).exists():
                    raise serializers.ValidationError(
                        "This track already exists in the library (acoustic fingerprint check).")

        return super().validate(attrs)
