#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import (
    CriteriaPlaylist)
from bodzify_api.serializer.criteria.output.with_descendants_and_parent import \
    CriteriaWithDescendantsAndParentSerializer
from bodzify_api.serializer.playlist.children.criteria.output.base import \
    CriteriaBaseSerializer
from bodzify_api.serializer.playlist.children.criteria.output.base import \
    Fields as BaseFields
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root import \
    CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer


class Fields:
    UUID = BaseFields.UUID
    LIB_TRACKS_COUNT = BaseFields.LIB_TRACKS_COUNT
    NAME = BaseFields.NAME
    CRITERIA = BaseFields.CRITERIA
    PARENT = BaseFields.PARENT
    ROOT = BaseFields.ROOT


class CriteriaPlaylistWithoutTracksSerializer(CriteriaBaseSerializer):
    criteria = CriteriaWithDescendantsAndParentSerializer()
    parent = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer()
    root = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer()

    def get_name(self, obj) -> str:
        return obj.name

    def to_representation(self, instance):
        assert isinstance(instance, CriteriaPlaylist), f"Expected a CriteriaPlaylist, got {type(instance)}"
        return super().to_representation(instance)

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.CRITERIA,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.LIB_TRACKS_COUNT]
