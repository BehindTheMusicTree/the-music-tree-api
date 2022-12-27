#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.playlist.PlaylistWithoutParentSerializer import (
    PlaylistWithoutParentSerializer
)


class PlaylistWithoutTracksSerializer(PlaylistWithoutParentSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        if obj.parent is not None:
            return PlaylistWithoutParentSerializer(obj.parent).data
        else:
            return None

    class Meta:
        model = Playlist    
        fields = [
            "uuid",
            "name",
            "type",
            "criteria",
            "parent",
            "addedOn",
            "trackCount",
        ]
