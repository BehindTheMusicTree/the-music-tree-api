#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist \
    import ATTRIBUTES_LABEL as CRITERIA_PLAYLIST_ATTRIBUTES_LABEL, CriteriaPlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildWithoutTrackSerializer \
    import PlaylistChildWithoutTrackSerializer, FIELDS as PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS


class FIELDS:
    UUID = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.UUID
    NAME = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.NAME
    ADDED_ON = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.ADDED_ON
    PARENT = CRITERIA_PLAYLIST_ATTRIBUTES_LABEL.PARENT
    LIBRARY_TRACKS_COUNT = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.LIBRARY_TRACKS_COUNT


class CriteriaPlaylistWithoutTracksSerializer(PlaylistChildWithoutTrackSerializer):

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.PARENT,
                  FIELDS.LIBRARY_TRACKS_COUNT]
