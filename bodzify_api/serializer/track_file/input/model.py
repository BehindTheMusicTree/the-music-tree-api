#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.TrackFile import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL, TrackFile


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    FILE = ATTRIBUTES_LABEL.FILE
    FINGERPRINT = ATTRIBUTES_LABEL.FINGERPRINT
    SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT = "should_cancel_if_duplicate_fingerprint"


class TrackFileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrackFile
        fields = [FIELDS.USER,
                  FIELDS.FILE,
                  FIELDS.FINGERPRINT]

    def validate(self, attrs):
        if FIELDS.FINGERPRINT in attrs:
            if FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT in attrs and attrs[
                    FIELDS.SHOULD_CANCEL_IF_DUPLICATE_FINGERPRINT]:
                fingerprint = attrs[FIELDS.FINGERPRINT]
                if TrackFile.objects.filter(fingerprint=fingerprint).exists():
                    raise serializers.ValidationError(
                        "This track already exists in the library (acoustic fingerprint check).")

        return super().validate(attrs)
