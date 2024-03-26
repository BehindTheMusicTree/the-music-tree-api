#!/usr/bin/env python

from bodzify_api.model.play.Play import Play, ATTRIBUTES_LABEL
from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist


class FIELDS:
    CONTENT_OBJECT_UUID = ATTRIBUTES_LABEL.CONTENT_OBJECT + '_uuid'


class PlayPostSerializer(serializers.ModelSerializer):
    content_object_uuid = serializers.CharField(max_length=22, required=True)

    class Meta:
        model = Play
        fields = [FIELDS.CONTENT_OBJECT_UUID]
