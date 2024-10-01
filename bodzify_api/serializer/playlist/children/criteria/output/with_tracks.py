#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.BasePlaylist import AttributesLabel as PlaylistAttributesLabels
from bodzify_api.serializer.playlist.children.criteria.output.without_tracks \
    import CriteriaPlaylistWithoutTracksSerializer, Fields as CriteriaPlaylistWithoutTracksFields


class Fields:
    UUID = CriteriaPlaylistWithoutTracksFields.UUID
    NAME = CriteriaPlaylistWithoutTracksFields.NAME
    CRITERIA = CriteriaPlaylistWithoutTracksFields.CRITERIA
    PARENT = CriteriaPlaylistWithoutTracksFields.PARENT
    ROOT = CriteriaPlaylistWithoutTracksFields.ROOT
    CREATED_ON = CriteriaPlaylistWithoutTracksFields.CREATED_ON
    LIB_TRACKS_COUNT = CriteriaPlaylistWithoutTracksFields.LIB_TRACKS_COUNT
    LIB_TRACKS = PlaylistAttributesLabels.LIB_TRACKS


class CriteriaPlaylistWithTracksSerializer(CriteriaPlaylistWithoutTracksSerializer):

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CRITERIA,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS]
