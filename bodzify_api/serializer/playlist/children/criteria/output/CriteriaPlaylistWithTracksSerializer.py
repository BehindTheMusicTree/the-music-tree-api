#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.BasePlaylist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutTracksSerializer \
    import CriteriaPlaylistWithoutTracksSerializer, FIELDS as CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS


class FIELDS:
    UUID = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.UUID
    NAME = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.NAME
    CRITERIA = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.CRITERIA
    PARENT = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.PARENT
    ROOT = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.ROOT
    CREATED_ON = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.LIB_TRACKS_COUNT
    LIB_TRACKS = PLAYLIST_ATTRIBUTES_LABEL.LIB_TRACKS


class CriteriaPlaylistWithTracksSerializer(CriteriaPlaylistWithoutTracksSerializer):

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CRITERIA,
                  FIELDS.PARENT,
                  FIELDS.ROOT,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS]
