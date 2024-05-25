#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.File import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL, File


class FIELDS:
    FILE = ATTRIBUTES_LABEL.FILE
    FILENAME = ATTRIBUTES_LABEL.FILENAME
    EXTENSION = ATTRIBUTES_LABEL.EXTENSION
    HAS_FLAC_MD5_BEEN_CORRECTED = ATTRIBUTES_LABEL.HAS_FLAC_MD5_BEEN_CORRECTED
    SIZE_IN_BYTES = ATTRIBUTES_LABEL.SIZE_IN_BYTES
    SIZE_IN_KO = ATTRIBUTES_LABEL.SIZE_IN_KO
    SIZE_IN_MO = ATTRIBUTES_LABEL.SIZE_IN_MO
    BITRATE_IN_KBPS = ATTRIBUTES_LABEL.BITRATE_IN_KBPS


class FileDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [FIELDS.FILE,
                  FIELDS.FILENAME,
                  FIELDS.EXTENSION,
                  FIELDS.HAS_FLAC_MD5_BEEN_CORRECTED,
                  FIELDS.SIZE_IN_BYTES,
                  #   FIELDS.SIZE_IN_KO,
                  #   FIELDS.SIZE_IN_MO,
                  FIELDS.BITRATE_IN_KBPS]
