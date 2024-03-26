#!/usr/bin/env python

from bodzify_api.model.play.Play import Play, ATTRIBUTES_LABEL
from rest_framework import serializers


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    CONTENT_TYPE = ATTRIBUTES_LABEL.CONTENT_TYPE
    OBJECT_UUID = ATTRIBUTES_LABEL.OBJECT_ID
    TIME = ATTRIBUTES_LABEL.TIME


class PlayDetailedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [FIELDS.UUID,
                  FIELDS.CONTENT_TYPE,
                  FIELDS.OBJECT_UUID,
                  FIELDS.TIME]
