#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.playlist.CriteriaPlaylist import CriteriaPlaylist, \
    ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, \
    FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.serializer.playlist.output.PlaylistWithoutParentSerializer import \
    PlaylistWithoutParentSerializer


class CriteriaPlaylistWithoutTracksSerializer(PlaylistWithoutParentSerializer):
    parent = serializers.SerializerMethodField()
    uuid = serializers.CharField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.UUID)
    added_on = serializers.DateTimeField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.ADDED_ON)
    track_count = serializers.IntegerField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.TRACK_COUNT)

    def get_parent(self, obj) -> PlaylistWithoutParentSerializer:
        if obj.parent is not None:
            return PlaylistWithoutParentSerializer(obj.parent).data
        else:
            return None

    class Meta:
        model = CriteriaPlaylist
        fields = [PLAYLIST_ATTRIBUTES_LABEL.UUID,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME,
                  PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON,
                  CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT,
                  PLAYLIST_ATTRIBUTES_LABEL.TRACK_COUNT]
