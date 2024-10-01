#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.playlist.children.child \
    import ChildPlaylistSerializer, Fields as ChildPlaylistFields


class Fields:
    UUID = ChildPlaylistFields.UUID
    NAME = ChildPlaylistFields.NAME
    CREATED_ON = ChildPlaylistFields.CREATED_ON
    LIB_TRACKS_COUNT = ChildPlaylistFields.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer(ChildPlaylistSerializer):

    def get_name(self, obj) -> str:
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT]
