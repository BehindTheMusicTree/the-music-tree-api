#!/usr/bin/env python

from bodzify_api.model.Play import Play, AttributesLabels
from rest_framework import serializers


class Fields:
    USER = AttributesLabels.USER
    CONTENT_TYPE = AttributesLabels.CONTENT_TYPE
    OBJECT_UUID = AttributesLabels.OBJECT_UUID


class PlayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_TYPE, Fields.OBJECT_UUID]
