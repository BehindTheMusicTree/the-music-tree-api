#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.children.child \
    import ChildPlaylistSerializer, FIELDS as CHILD_PLAYLIST_FIELDS


class FIELDS:
    UUID = CHILD_PLAYLIST_FIELDS.UUID
    NAME = CHILD_PLAYLIST_FIELDS.NAME
    CREATED_ON = CHILD_PLAYLIST_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = CHILD_PLAYLIST_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer(ChildPlaylistSerializer):

    def get_name(self, obj) -> str:
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS_COUNT]
