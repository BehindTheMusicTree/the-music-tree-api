#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.model.playlist.children.CriteriaPlaylist import ATTRIBUTES_LABEL, CriteriaPlaylist
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.playlist.children.PlaylistChildSerializer \
    import PlaylistChildSerializer, FIELDS as PLAYLIST_CHILD_FIELDS


class FIELDS:
    UUID = PLAYLIST_CHILD_FIELDS.UUID
    NAME = PLAYLIST_CHILD_FIELDS.NAME
    ADDED_ON = PLAYLIST_CHILD_FIELDS.ADDED_ON
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer(PlaylistChildSerializer):

    def get_name(self, obj):
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.LIB_TRACKS_COUNT]
