#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, \
    FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.model.playlist.SimplePlaylist import SimplePlaylist, \
    ATTRIBUTES_LABELS as SIMPLE_PLAYLIST_ATTRIBUTES_LABEL

class SimplePlaylistWithoutParentSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.UUID)
    added_on = serializers.DateTimeField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.ADDED_ON)
    track_count = serializers.IntegerField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.TRACK_COUNT)

    class Meta:
        model = SimplePlaylist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  SIMPLE_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  PLAYLIST_ATTRIBUTES_LABEL.TRACK_COUNT]
