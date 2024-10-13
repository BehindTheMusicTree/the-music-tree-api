#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.children.criteria.output.base import CriteriaBaseSerializer
from bodzify_api.serializer.playlist.children.criteria.output.base import Fields as BaseFields
from bodzify_api.serializer.playlist.children.criteria.output.base import Sources as BaseSources
from bodzify_api.serializer.track.output.simple_without_playlists_and_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class Fields:
    UUID = BaseFields.UUID
    CREATED_ON = BaseFields.CREATED_ON
    UPDATED_ON = BaseFields.UPDATED_ON
    LIB_TRACKS = BaseFields.LIB_TRACKS
    LIB_TRACKS_COUNT = BaseFields.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = BaseFields.LIB_TRACKS_ARCHIVED_COUNT
    DURATION_IN_SEC = BaseFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = BaseFields.DURATION_STR_IN_HOUR_MIN_SEC
    NAME = BaseFields.NAME
    CRITERIA = BaseFields.CRITERIA
    PARENT = BaseFields.PARENT
    ROOT = BaseFields.ROOT


class CriteriaPlaylistDetailedSerializer(CriteriaBaseSerializer):
    library_tracks = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(source=BaseSources.LIB_TRACKS_NOT_ARCHIVED,
                                                                     many=True)

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CRITERIA,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
