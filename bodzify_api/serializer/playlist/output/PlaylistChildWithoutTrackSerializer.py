#!/usr/bin/env python

from typing import Optional
from rest_framework import serializers

from bodzify_api.model.playlist.CriteriaPlaylist import ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, Playlist
from bodzify_api.model.playlist.Playlist import FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.serializer.playlist.output.PlaylistSerializer import PlaylistSerializer


class PlaylistChildWithoutTrackSerializer(PlaylistSerializer):
    parent = serializers.SerializerMethodField()
    uuid = serializers.CharField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.UUID)
    added_on = serializers.DateTimeField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.ADDED_ON)
    library_tracks_count = serializers.IntegerField(
        source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.LIBRARY_TRACKS + '.count')

    def get_parent(self, obj) -> Optional[PlaylistSerializer]:
        if obj.parent is not None:
            return PlaylistSerializer(obj.parent).data
        else:
            return None

    class Meta:
        model = Playlist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT,
                  PLAYLIST_ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT]
