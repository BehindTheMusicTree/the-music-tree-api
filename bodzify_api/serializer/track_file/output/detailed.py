#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track_file.TrackFile import AttributesLabel as AttributesLabel, TrackFile
from bodzify_api.serializer.fingerprinting_error_code.detailed import FingerprintingErrorCodeDetailedSerializer


class FIELDS:
    FILENAME = AttributesLabel.FILENAME
    EXTENSION = AttributesLabel.EXTENSION
    FINGERPRINTING_ERROR_CODE = AttributesLabel.FINGERPRINTING_ERROR_CODE
    FLAC_MD5_HAS_BEEN_CORRECTED = AttributesLabel.FLAC_MD5_HAS_BEEN_CORRECTED
    SIZE_IN_BYTES = AttributesLabel.SIZE_IN_BYTES
    SIZE_IN_KO = AttributesLabel.SIZE_IN_KO
    SIZE_IN_MO = AttributesLabel.SIZE_IN_MO
    BITRATE_IN_KBPS = AttributesLabel.BITRATE_IN_KBPS


class FileDetailedSerializer(serializers.ModelSerializer):

    fingerprinting_error_code = FingerprintingErrorCodeDetailedSerializer()

    class Meta:
        model = TrackFile
        fields = [FIELDS.FILENAME,
                  FIELDS.EXTENSION,
                  FIELDS.FINGERPRINTING_ERROR_CODE,
                  FIELDS.FLAC_MD5_HAS_BEEN_CORRECTED,
                  FIELDS.SIZE_IN_BYTES,
                  FIELDS.SIZE_IN_KO,
                  FIELDS.SIZE_IN_MO,
                  FIELDS.BITRATE_IN_KBPS]
