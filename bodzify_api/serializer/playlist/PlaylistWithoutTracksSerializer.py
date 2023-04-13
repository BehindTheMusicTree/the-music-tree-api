#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.playlist.Playlist import Playlist, ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.PlaylistWithoutParentSerializer import (
    PlaylistWithoutParentSerializer)


class PlaylistWithoutTracksSerializer(PlaylistWithoutParentSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj) -> PlaylistWithoutParentSerializer:
        if obj.parent is not None:
            return PlaylistWithoutParentSerializer(obj.parent).data
        else:
            return None

    class Meta:
        model = Playlist
        fields = [ATTRIBUTES_LABEL.UUID,
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.TYPE,
                  ATTRIBUTES_LABEL.ADDED_ON,
                  "trackCount"]
