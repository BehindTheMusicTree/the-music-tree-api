#!/usr/bin/env python

from bodzify_api.model.Play import Play, AttributesLabel
from rest_framework import serializers


class Fields:
    USER = AttributesLabel.USER
    CONTENT_TYPE = AttributesLabel.CONTENT_TYPE
    OBJECT_UUID = AttributesLabel.OBJECT_UUID


class PlayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_TYPE, Fields.OBJECT_UUID]
