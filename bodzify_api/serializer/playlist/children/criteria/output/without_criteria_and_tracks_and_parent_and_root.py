#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import \
    CriteriaPlaylist
from bodzify_api.serializer.playlist.children.criteria.output.base import \
    CriteriaBaseSerializer
from bodzify_api.serializer.playlist.children.criteria.output.base import \
    Fields as BaseFields


class Fields:
    UUID = BaseFields.UUID
    NAME = BaseFields.NAME
    LIB_TRACKS_COUNT = BaseFields.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer(CriteriaBaseSerializer):

    def get_name(self, obj) -> str:
        return obj.name

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT]
