#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track_file.FingerprintingErrorCode import FingerprintingErrorCode, ATTRIBUTES_LABEL


class FIELDS:
    LABEL = ATTRIBUTES_LABEL.LABEL


class FingerprintingErrorCodeDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingerprintingErrorCode
        fields = [FIELDS.LABEL]
