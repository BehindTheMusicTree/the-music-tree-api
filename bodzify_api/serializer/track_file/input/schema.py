#!/usr/bin/env python

import binascii
from rest_framework import serializers

from bodzify_api.model.track_file.TrackFile import AttributesLabel as AttributesLabel, TrackFile


class FIELDS:
    FILE = AttributesLabel.FILE
    FINGERPRINT_CHAR = AttributesLabel.FINGERPRINT
    FINGERPRINTING_ERROR_CODE = AttributesLabel.FINGERPRINTING_ERROR_CODE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = "should_cancel_if_duplicate_fingerprint"


class TrackFileSchemaSerializer(serializers.Serializer):
    file = serializers.FileField()

    # Django serializers don't support binary fields. We pass the fingerprint as a string and convert it to binary
    # creating the instance of the model.
    fingerprint = serializers.CharField(required=False)
    fingerprinting_error_code = serializers.IntegerField(required=False)
    should_cancel_if_duplicate_fingerprint = serializers.BooleanField(required=False)

    def validate(self, attrs):
        if FIELDS.FINGERPRINT_CHAR in attrs:
            if FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT in attrs and attrs[
                    FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT]:
                user = self.context['user']
                fingerprint = binascii.unhexlify(attrs[FIELDS.FINGERPRINT_CHAR])
                if TrackFile.objects.filter(user=user, fingerprint=fingerprint).exists():
                    raise serializers.ValidationError(
                        "This track already exists in the library (acoustic fingerprint check).")
        return super().validate(attrs)
