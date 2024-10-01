#!/usr/bin/env python

from bodzify_api.model.playlist.children.CriteriaPlaylist import AttributesLabel, CriteriaPlaylist
from bodzify_api.serializer.criteria.output.with_descendants import CriteriaWithDescendantsSerializer
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root \
    import Fields as CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootFields
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root \
    import CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer


class Fields:
    UUID = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootFields.UUID
    NAME = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootFields.NAME
    CRITERIA = AttributesLabel.CRITERIA
    CREATED_ON = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootFields.CREATED_ON
    PARENT = AttributesLabel.PARENT
    ROOT = AttributesLabel.ROOT
    LIB_TRACKS_COUNT = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootFields.LIB_TRACKS_COUNT


class CriteriaPlaylistWithoutTracksSerializer(CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer):
    criteria = CriteriaWithDescendantsSerializer()
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
                  Fields.CREATED_ON,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.LIB_TRACKS_COUNT]
