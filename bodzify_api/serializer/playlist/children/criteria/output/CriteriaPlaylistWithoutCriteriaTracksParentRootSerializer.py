#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import ForeignModelRelationsStr as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.model.playlist.children.CriteriaPlaylist import AttributesLabel, CriteriaPlaylist
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.playlist.children.PlaylistChildSerializer \
    import PlaylistChildSerializer, Fields as PLAYLIST_CHILD_FIELDS


class Fields:
    UUID = PLAYLIST_CHILD_FIELDS.UUID
    NAME = PLAYLIST_CHILD_FIELDS.NAME
    ADDED_ON = PLAYLIST_CHILD_FIELDS.ADDED_ON
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer(PlaylistChildSerializer):

    def get_name(self, obj):
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ADDED_ON,
                  Fields.LIB_TRACKS_COUNT]
