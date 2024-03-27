#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import ATTRIBUTES_LABEL, CriteriaPlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildWithoutTrackSerializer \
    import PlaylistChildWithoutTrackSerializer, FIELDS as PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS


class FIELDS:
    UUID = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.UUID
    NAME = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.NAME
    ADDED_ON = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.ADDED_ON
    PARENT = ATTRIBUTES_LABEL.PARENT
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_WITHOUT_TRACK_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutTracksSerializer(PlaylistChildWithoutTrackSerializer):
    def get_name(self, obj):
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.PARENT,
                  FIELDS.LIB_TRACKS_COUNT]
