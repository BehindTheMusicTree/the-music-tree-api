#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.playlist.PlaylistTypeSerializer import PlaylistTypeSerializer


class PlaylistWithoutParentSerializer(serializers.ModelSerializer):
    type = PlaylistTypeSerializer()
    trackCount = serializers.IntegerField(source='librarytrack_set.count')

    class Meta:
        model = Playlist
        fields = [
            "uuid",
            "name",
            "type",
            "criteria",
            "addedOn",
            "trackCount"
        ]
