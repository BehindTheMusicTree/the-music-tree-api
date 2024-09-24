#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track_file.FingerprintingErrorCode import FingerprintingErrorCode, AttributesLabel


class FIELDS:
    LABEL = AttributesLabel.LABEL


class FingerprintingErrorCodeDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingerprintingErrorCode
        fields = [FIELDS.LABEL]
