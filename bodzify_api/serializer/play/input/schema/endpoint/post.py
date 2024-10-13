#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api import settings
from bodzify_api.model.Play import AttributesLabels, Play
from bodzify_api.serializer.endpoint import InputEndpointSerializer


class Fields:
    CONTENT_OBJECT_UUID = AttributesLabels.CONTENT_OBJECT + '_uuid'


class PlayPostSerializer(InputEndpointSerializer):
    content_object_uuid = serializers.CharField(max_length=settings.UUID_LEN, required=True)

    class Meta:
        model = Play
        fields = [Fields.CONTENT_OBJECT_UUID]
