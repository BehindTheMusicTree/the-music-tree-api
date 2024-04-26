#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.File import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL, File


class FIELDS:
    USER = ATTRIBUTES_LABEL.USER
    FILE = ATTRIBUTES_LABEL.FILE


class FileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [FIELDS.USER,
                  FIELDS.FILE]
