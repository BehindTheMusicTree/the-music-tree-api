#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, \
    FOREIGN_MODEL_RELATIONS_STR as PLAYLIST_FOREIGN_MODEL_RELATIONS_STR
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutTracksSerializer \
    import CriteriaPlaylistWithoutTracksSerializer, FIELDS as CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS
from bodzify_api.serializer.track.output.LibTrackWithoutAlbumAndPlaylistSerializer import \
    LibTrackWithoutAlbumAndPlaylistSerializer


class FIELDS:
    UUID = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.UUID
    NAME = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.NAME
    PARENT = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.PARENT
    ADDED_ON = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.ADDED_ON
    LIB_TRACKS_COUNT = CRITERIA_PLAYLIST_WITHOUT_TRACKS_FIELDS.LIB_TRACKS_COUNT
    LIB_TRACKS = PLAYLIST_ATTRIBUTES_LABEL.LIB_TRACKS


class CriteriaPlaylistWithTracksSerializer(CriteriaPlaylistWithoutTracksSerializer):

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.PARENT,
                  FIELDS.ADDED_ON,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.LIB_TRACKS]
