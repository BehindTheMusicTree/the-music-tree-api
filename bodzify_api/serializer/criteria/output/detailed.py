#!/usr/bin/env python

from typing import Any, Dict, List
from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria, AttributesLabel
from bodzify_api.model.track.LibraryTrack import AttributesLabel as LIBRARY_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria.type.detailed \
    import CriteriaTypeSerializer, FIELDS as CRITERIA_TYPE_FIELDS
from bodzify_api.serializer.criteria_ascendant_relation.detailed import CriteriaAscendantRelationDetailedSerializer
from bodzify_api.serializer.criteria_ascendant_relation.without_ascendant import CriteriaAscendantRelationWithoutAscendantSerializer
from bodzify_api.serializer.criteria_ascendant_relation.without_descendant import CriteriaAscendantRelationWithoutDescendantSerializer
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root import CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer

from bodzify_api.serializer.track.output.without_playlists_and_album_and_genre \
    import LibTrackWithoutAlbumPlaylistGenreSerializer


class FIELDS:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    PARENT = AttributesLabel.PARENT
    ASCENDANTS = AttributesLabel.ASCENDANTS
    DESCENDANTS = AttributesLabel.DESCENDANTS
    ROOT = AttributesLabel.ROOT
    CHILDREN = AttributesLabel.CHILDREN
    TYPE = AttributesLabel.TYPE
    TYPE_LABEL = CRITERIA_TYPE_FIELDS.LABEL
    CREATED_ON = AttributesLabel.CREATED_ON
    LIB_TRACKS = AttributesLabel.LIB_TRACKS
    LIB_TRACKS_TITLE = LIBRARY_TRACK_ATTRIBUTES_LABEL.TITLE
    CRITERIA_PLAYLIST = AttributesLabel.CRITERIA_PLAYLIST


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    type = CriteriaTypeSerializer()
    parent = CriteriaSimpleSerializer()
    ascendants = CriteriaAscendantRelationWithoutDescendantSerializer(
        source=AttributesLabel.CRITERIA_ASCENDANT_RELATION_ASCENDANTS,
        many=True)
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=AttributesLabel.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)
    root = CriteriaSimpleSerializer()  # type: ignore
    children = serializers.SerializerMethodField()
    criteria_playlist = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer()
    library_tracks = LibTrackWithoutAlbumPlaylistGenreSerializer(many=True)

    class Meta:
        model = Criteria
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.PARENT,
                  FIELDS.ASCENDANTS,
                  FIELDS.DESCENDANTS,
                  FIELDS.ROOT,
                  FIELDS.CHILDREN,
                  FIELDS.TYPE,
                  FIELDS.CREATED_ON,
                  FIELDS.LIB_TRACKS,
                  FIELDS.CRITERIA_PLAYLIST]

    def get_children(self, obj) -> List[Dict[str, Any]]:
        return CriteriaSimpleSerializer(obj.get_children(), many=True).data  # type: ignore
