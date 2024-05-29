#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.children.PlaylistChildSerializer \
    import PlaylistChildSerializer, FIELDS as PLAYLIST_CHILD_FIELDS


class FIELDS:
    UUID = PLAYLIST_CHILD_FIELDS.UUID
    NAME = PLAYLIST_CHILD_FIELDS.NAME
    CREATED_ON = PLAYLIST_CHILD_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = PLAYLIST_CHILD_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer(PlaylistChildSerializer):

    def get_name(self, obj) -> str:
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT]
