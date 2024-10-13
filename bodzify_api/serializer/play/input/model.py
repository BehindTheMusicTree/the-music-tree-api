#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.Play import AttributesLabels, Play


class Fields:
    USER = AttributesLabels.USER
    CONTENT_TYPE = AttributesLabels.CONTENT_TYPE
    OBJECT_UUID = AttributesLabels.OBJECT_UUID


class PlayModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = [Fields.USER, Fields.CONTENT_TYPE, Fields.OBJECT_UUID]
