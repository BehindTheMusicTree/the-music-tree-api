#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import AttributesLabels
from bodzify_api.serializer.playlist.children.child import ChildPlaylistSerializer
from bodzify_api.serializer.playlist.children.child import Fields as ChildPlaylistFields
from bodzify_api.serializer.playlist.children.child import Sources as ChildPlaylistSources


class Fields:
    UUID = ChildPlaylistFields.UUID
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    UPDATED_ON = ChildPlaylistFields.UPDATED_ON
    LIB_TRACKS = ChildPlaylistFields.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = ChildPlaylistFields.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = ChildPlaylistFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildPlaylistFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = ChildPlaylistFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ChildPlaylistFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = ChildPlaylistFields.NAME
    CRITERIA = AttributesLabels.CRITERIA
    PARENT = AttributesLabels.PARENT
    ROOT = AttributesLabels.ROOT


class Sources:
    CREATED_ON = ChildPlaylistSources.CREATED_ON
    UPDATED_ON = ChildPlaylistSources.UPDATED_ON
    LIB_TRACKS_NOT_ARCHIVED = ChildPlaylistSources.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = ChildPlaylistSources.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = ChildPlaylistSources.LIB_TRACKS_ARCHIVED_COUNT


class CriteriaBaseSerializer(ChildPlaylistSerializer):

    def get_name(self, obj) -> str:
        return obj.name
