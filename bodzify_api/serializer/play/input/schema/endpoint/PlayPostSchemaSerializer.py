#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.Play import Play, ATTRIBUTES_LABEL
from bodzify_api.serializer.InputEndpointSerializer import InputEndpointSerializer


class FIELDS:
    CONTENT_OBJECT_UUID = ATTRIBUTES_LABEL.CONTENT_OBJECT + '_uuid'


class PlayPostSerializer(InputEndpointSerializer):
    content_object_uuid = serializers.CharField(max_length=settings.UUID_LEN, required=True)

    class Meta:
        model = Play
        fields = [FIELDS.CONTENT_OBJECT_UUID]
