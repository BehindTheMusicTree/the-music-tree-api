#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.playlist.Playlist import Playlist, \
    ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.PlaylistTypeSerializer import PlaylistTypeSerializer


class ATTRIBUTES_LABEL:
    TRACK_COUNT = "trackCount"

class PlaylistWithoutParentSerializer(serializers.ModelSerializer):
    type = PlaylistTypeSerializer()
    trackCount = serializers.IntegerField(source='librarytrack_set.count')

    class Meta:
        model = Playlist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_ATTRIBUTES_LABEL.TYPE,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  ATTRIBUTES_LABEL.TRACK_COUNT]
