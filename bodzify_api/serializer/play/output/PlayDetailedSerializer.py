#!/usr/bin/env python

from bodzify_api.model.play.Play import Play, ATTRIBUTES_LABEL
from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.playlist.mother.output.PlaylistWithoutTrackSerializer import PlaylistWithoutTrackSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    CONTENT_TYPE = ATTRIBUTES_LABEL.CONTENT_TYPE
    CONTENT_OBJECT = ATTRIBUTES_LABEL.CONTENT_OBJECT
    TIME = ATTRIBUTES_LABEL.TIME


class PlayDetailedSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type.model')
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = [FIELDS.UUID,
                  FIELDS.CONTENT_TYPE,
                  FIELDS.CONTENT_OBJECT,
                  FIELDS.TIME]

    def get_content_object(self, obj):
        if isinstance(obj.content_object, Playlist):
            return PlaylistWithoutTrackSerializer(obj.content_object).data
        return None
