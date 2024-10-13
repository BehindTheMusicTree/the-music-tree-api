#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import \
    AttributesLabels as BaseAttributesLabels
from bodzify_api.model.playlist.BasePlaylist import \
    ForeignModelRelationsStr as PlaylistForeignModelRelStr
from bodzify_api.model.playlist.children.CriteriaPlaylist import \
    AttributesLabels as CRITERIA_PlaylistAttributesLabels
from bodzify_api.serializer.playlist.base.output.without_tracks import \
    BasePlaylistWithOnlyNameAndType


class Fields:
    UUID = BaseAttributesLabels.UUID
    NAME = CRITERIA_PlaylistAttributesLabels.NAME
    CREATED_ON = BaseAttributesLabels.CREATED_ON
    UPDATED_ON = BaseAttributesLabels.UPDATED_ON
    LIB_TRACKS = BaseAttributesLabels.LIB_TRACKS
    LIB_TRACKS_NOT_ARCHIVED = BaseAttributesLabels.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = BaseAttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED = BaseAttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = BaseAttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = BaseAttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = BaseAttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC


class Sources:
    CREATED_ON = PlaylistForeignModelRelStr.CREATED_ON
    UPDATED_ON = PlaylistForeignModelRelStr.UPDATED_ON
    LIB_TRACKS_NOT_ARCHIVED = PlaylistForeignModelRelStr.LIB_TRACKS_NOT_ARCHIVED
    LIB_TRACKS_COUNT = PlaylistForeignModelRelStr.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = PlaylistForeignModelRelStr.LIB_TRACKS_ARCHIVED_COUNT


class ChildPlaylistSerializer(BasePlaylistWithOnlyNameAndType):
    uuid = serializers.CharField(source=PlaylistForeignModelRelStr.UUID)

    def get_library_tracks_count(self, obj) -> int:
        return obj.base_playlist.library_tracks.count()

    class Meta:
        fields = [Fields.UUID,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC]
