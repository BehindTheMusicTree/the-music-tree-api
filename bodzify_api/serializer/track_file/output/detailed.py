#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track_file.TrackFile import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL, TrackFile
from bodzify_api.serializer.fingerprinting_error_code.detailed import FingerprintingErrorCodeDetailedSerializer


class FIELDS:
    FILENAME = ATTRIBUTES_LABEL.FILENAME
    EXTENSION = ATTRIBUTES_LABEL.EXTENSION
    FINGERPRINTING_ERROR_CODE = ATTRIBUTES_LABEL.FINGERPRINTING_ERROR_CODE
    FLAC_MD5_HAS_BEEN_CORRECTED = ATTRIBUTES_LABEL.FLAC_MD5_HAS_BEEN_CORRECTED
    SIZE_IN_BYTES = ATTRIBUTES_LABEL.SIZE_IN_BYTES
    SIZE_IN_KO = ATTRIBUTES_LABEL.SIZE_IN_KO
    SIZE_IN_MO = ATTRIBUTES_LABEL.SIZE_IN_MO
    BITRATE_IN_KBPS = ATTRIBUTES_LABEL.BITRATE_IN_KBPS


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
