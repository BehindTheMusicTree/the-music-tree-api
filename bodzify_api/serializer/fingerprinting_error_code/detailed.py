#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.track_file.FingerprintingErrorCode import FingerprintingErrorCode, AttributesLabels


class Fields:
    LABEL = AttributesLabels.LABEL


class FingerprintingErrorCodeDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingerprintingErrorCode
        fields = [Fields.LABEL]
