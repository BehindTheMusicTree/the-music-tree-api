#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track_file.TrackFile import AttributesLabels as AttributesLabels, TrackFile
from bodzify_api.serializer.fingerprinting_error.detailed import FingerprintingErrorDetailedSerializer


class Fields:
    FILENAME = AttributesLabels.FILENAME
    EXTENSION = AttributesLabels.EXTENSION
    FINGERPRINTING_ERROR_CODE = AttributesLabels.FINGERPRINTING_ERROR_CODE
    FLAC_MD5_HAS_BEEN_CORRECTED = AttributesLabels.FLAC_MD5_HAS_BEEN_CORRECTED
    SIZE_IN_BYTES = AttributesLabels.SIZE_IN_BYTES
    SIZE_IN_KO = AttributesLabels.SIZE_IN_KO
    SIZE_IN_MO = AttributesLabels.SIZE_IN_MO
    BITRATE_IN_KBPS = AttributesLabels.BITRATE_IN_KBPS


class FileDetailedSerializer(serializers.ModelSerializer):

    fingerprinting_error = FingerprintingErrorDetailedSerializer()

    class Meta:
        model = TrackFile
        fields = [Fields.FILENAME,
                  Fields.EXTENSION,
                  Fields.FINGERPRINTING_ERROR_CODE,
                  Fields.FLAC_MD5_HAS_BEEN_CORRECTED,
                  Fields.SIZE_IN_BYTES,
                  Fields.SIZE_IN_KO,
                  Fields.SIZE_IN_MO,
                  Fields.BITRATE_IN_KBPS]
