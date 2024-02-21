#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    library_tracks_count = serializers.IntegerField(source=ATTRIBUTES_LABEL.LIBRARY_TRACKS + '.count')

    class Meta:
        model = Playlist
        fields = [ATTRIBUTES_LABEL.UUID,
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.ADDED_ON,
                  ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT]
