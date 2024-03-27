#!/usr/bin/env python

from typing import Optional
import logging
from rest_framework import serializers

from bodzify_api.model.playlist.children.CriteriaPlaylist import ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.model.playlist.Playlist import FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.serializer.playlist.mother.output.PlaylistWithoutTrackSerializer import PlaylistWithoutTrackSerializer

logger = logging.getLogger('bodzify_api')


class FIELDS:
    UUID = PLAYLIST_ATTRIBUTES_LABEL.UUID
    NAME = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME
    ADDED_ON = PLAYLIST_ATTRIBUTES_LABEL.ADDED_ON
    PARENT = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT
    LIB_TRACKS_COUNT = PLAYLIST_ATTRIBUTES_LABEL.LIB_TRACKS_COUNT


class PlaylistChildWithoutTrackSerializer(PlaylistWithoutTrackSerializer):
    parent = serializers.SerializerMethodField()
    uuid = serializers.CharField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.UUID)
    added_on = serializers.DateTimeField(source=PLAYLIST_FOREIGN_MODEL_RELATIONS_STR.ADDED_ON)
    library_tracks_count = serializers.SerializerMethodField()

    def get_library_tracks_count(self, obj):
        return obj.playlist.library_tracks.count()

    def get_parent(self, obj) -> Optional[PlaylistWithoutTrackSerializer]:
        if obj.parent is not None:
            return PlaylistWithoutTrackSerializer(obj.parent).data
        else:
            return None

    class Meta:
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.PARENT,
                  FIELDS.LIB_TRACKS_COUNT]
