#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCauseCode import FingerprintMissingCauseCode, Fields as ModelFields


class Fields:
    CODE = ModelFields.CODE
    LABEL = ModelFields.LABEL


class FingerprintMissingCauseCodeDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingerprintMissingCauseCode
        fields = [Fields.CODE, Fields.LABEL]
