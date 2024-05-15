#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import ATTRIBUTES_LABEL, CriteriaPlaylist
from bodzify_api.serializer.criteria.output.CriteriaSimpleSerializer import CriteriaSimpleSerializer
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer \
    import FIELDS as CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer \
    import CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer


class FIELDS:
    UUID = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.UUID
    NAME = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.NAME
    CRITERIA = ATTRIBUTES_LABEL.CRITERIA
    ADDED_ON = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.ADDED_ON
    PARENT = ATTRIBUTES_LABEL.PARENT
    ROOT = ATTRIBUTES_LABEL.ROOT
    LIB_TRACKS_COUNT = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutTracksSerializer(CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer):
    criteria = CriteriaSimpleSerializer()
    parent = CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer()
    root = CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer()

    def get_name(self, obj):
        return obj.name

    def to_representation(self, instance):
        assert isinstance(instance, CriteriaPlaylist), f"Expected a CriteriaPlaylist, got {type(instance)}"
        return super().to_representation(instance)

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CRITERIA,
                  FIELDS.ADDED_ON,
                  FIELDS.PARENT,
                  FIELDS.ROOT,
                  FIELDS.LIB_TRACKS_COUNT]
