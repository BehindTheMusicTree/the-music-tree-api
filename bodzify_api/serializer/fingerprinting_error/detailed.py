#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track_file.FingerprintingError import (
    AttributesLabels, FingerprintingError)


class Fields:
    ID = AttributesLabels.ID
    LABEL = AttributesLabels.LABEL


class FingerprintingErrorDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = FingerprintingError
        fields = [Fields.ID, Fields.LABEL]
