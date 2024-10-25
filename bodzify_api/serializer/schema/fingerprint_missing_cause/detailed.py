#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.file.fingerprinting.missing_cause.FingerprintMissingCause import FingerprintMissingCause, Fields as ModelFields
from bodzify_api.serializer.schema.fingerprint_missing_cause.code.detailed import FingerprintMissingCauseCodeDetailedSerializer


class Fields:
    CODE = ModelFields.CODE
    MESSAGE = ModelFields.MESSAGE


class FingerprintMissingCauseDetailedSerializer(serializers.ModelSerializer):
    code = FingerprintMissingCauseCodeDetailedSerializer()

    class Meta:
        model = FingerprintMissingCause
        fields = [Fields.CODE, Fields.MESSAGE]
