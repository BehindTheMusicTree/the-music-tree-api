#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.TrackFile import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL, TrackFile


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    FILE = ATTRIBUTES_LABEL.FILE
    FINGERPRINT = ATTRIBUTES_LABEL.FINGERPRINT
    SHOULD_CHECK_IF_FINGERPRINT_EXISTS = "should_check_if_fingerprint_exists"


class FileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackFile
        fields = [FIELDS.USER,
                  FIELDS.FILE,
                  FIELDS.FINGERPRINT]

    def validate(self, attrs):
        if FIELDS.FINGERPRINT in attrs:
            if FIELDS.SHOULD_CHECK_IF_FINGERPRINT_EXISTS in attrs and attrs[
                    FIELDS.SHOULD_CHECK_IF_FINGERPRINT_EXISTS]:
                fingerprint = attrs[FIELDS.FINGERPRINT]
                if TrackFile.objects.filter(fingerprint=fingerprint).exists():
                    raise serializers.ValidationError(
                        "This track already exists in the library (acoustic fingerprint check).")

        return super().validate(attrs)
