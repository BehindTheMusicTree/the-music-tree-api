#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.children.child \
    import ChildPlaylistSerializer, Fields as CHILD_PLAYLIST_FIELDS


class Fields:
    UUID = CHILD_PLAYLIST_FIELDS.UUID
    NAME = CHILD_PLAYLIST_FIELDS.NAME
    CREATED_ON = CHILD_PLAYLIST_FIELDS.CREATED_ON
    LIB_TRACKS_COUNT = CHILD_PLAYLIST_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer(ChildPlaylistSerializer):

    def get_name(self, obj) -> str:
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT]
