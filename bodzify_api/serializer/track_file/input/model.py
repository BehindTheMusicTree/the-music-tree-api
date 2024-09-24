#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track_file.TrackFile import AttributesLabel as AttributesLabel, TrackFile


class Fields:
    USER = AttributesLabel.USER
    FILE = AttributesLabel.FILE
    FINGERPRINT = AttributesLabel.FINGERPRINT
    FINGERPRINTING_ERROR_CODE = AttributesLabel.FINGERPRINTING_ERROR_CODE
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = "should_cancel_if_duplicate_fingerprint"


class TrackFileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackFile
        fields = [Fields.USER,
                  Fields.FILE,
                  Fields.FINGERPRINT,
                  Fields.FINGERPRINTING_ERROR_CODE]

    def validate(self, attrs):
        if Fields.FINGERPRINT in attrs:
            if Fields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT in attrs and attrs[
                    Fields.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT]:
                fingerprint = attrs[Fields.FINGERPRINT]
                user = attrs[Fields.USER]
                if TrackFile.objects.filter(user=user, fingerprint=fingerprint).exists():
                    raise serializers.ValidationError(
                        "This track already exists in the library (acoustic fingerprint check).")
        return super().validate(attrs)
