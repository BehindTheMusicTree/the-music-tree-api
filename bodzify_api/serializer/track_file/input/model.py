#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track_file.TrackFile import AttributesLabel as AttributesLabel, TrackFile


class FIELDS:
    USER = AttributesLabel.USER
    FILE = AttributesLabel.FILE
    FINGERPRINT = AttributesLabel.FINGERPRINT
    FINGERPRINTING_ERROR_CODE = AttributesLabel.FINGERPRINTING_ERROR_CODE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = "should_cancel_if_duplicate_fingerprint"


class TrackFileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackFile
        fields = [FIELDS.USER,
                  FIELDS.FILE,
                  FIELDS.FINGERPRINT,
                  FIELDS.FINGERPRINTING_ERROR_CODE]

    def validate(self, attrs):
        if FIELDS.FINGERPRINT in attrs:
            if FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT in attrs and attrs[
                    FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT]:
                fingerprint = attrs[FIELDS.FINGERPRINT]
                user = attrs[FIELDS.USER]
                if TrackFile.objects.filter(user=user, fingerprint=fingerprint).exists():
                    raise serializers.ValidationError(
                        "This track already exists in the library (acoustic fingerprint check).")
        return super().validate(attrs)
