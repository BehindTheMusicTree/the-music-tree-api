#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import AttributesLabel, CriteriaPlaylist
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root \
    import FIELDS as CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root \
    import CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer


class FIELDS:
    UUID = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.UUID
    NAME = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.NAME
    CRITERIA = AttributesLabel.CRITERIA
    CREATED_ON = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.CREATED_ON
    PARENT = AttributesLabel.PARENT
    ROOT = AttributesLabel.ROOT
    LIB_TRACKS_COUNT = CRITERIA_PLAYLIST_WITHOUT_CRITERIA_TRACKS_PARENT_ROOT_FIELDS.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutTracksSerializer(CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer):
    criteria = CriteriaSimpleSerializer()
    parent = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer()
    root = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer()

    def get_name(self, obj) -> str:
        return obj.name

    def to_representation(self, instance):
        assert isinstance(instance, CriteriaPlaylist), f"Expected a CriteriaPlaylist, got {type(instance)}"
        return super().to_representation(instance)

    class Meta:
        model = CriteriaPlaylist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.CRITERIA,
                  FIELDS.CREATED_ON,
                  FIELDS.PARENT,
                  FIELDS.ROOT,
                  FIELDS.LIB_TRACKS_COUNT]
