#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.playlist.Playlist import Playlist, \
    ATTRIBUTES_LABEL as ATTRIBUTES_LABEL

class PlaylistWithoutParentSerializer(serializers.ModelSerializer):
    track_count = serializers.IntegerField(source='librarytrack_set.count')

    class Meta:
        model = Playlist
        fields = [ATTRIBUTES_LABEL.UUID,
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.ADDED_ON,
                  ATTRIBUTES_LABEL.TRACK_COUNT]
