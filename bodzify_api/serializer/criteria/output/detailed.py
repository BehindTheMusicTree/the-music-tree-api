#!/usr/bin/env python

from typing import Any, Dict, List

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import AttributesLabels, Criteria
from bodzify_api.model.track.LibraryTrack import AttributesLabels as LibTrackAttributesLabels
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria.type.detailed import CriteriaTypeSerializer
from bodzify_api.serializer.criteria.type.detailed import Fields as CriteriaTypeFields
from bodzify_api.serializer.criteria_ascendant_relation.without_ascendant import \
    CriteriaAscendantRelationWithoutAscendantSerializer
from bodzify_api.serializer.criteria_ascendant_relation.without_descendant import \
    CriteriaAscendantRelationWithoutDescendantSerializer
from bodzify_api.serializer.playlist.children.criteria.output.without_criteria_and_tracks_and_parent_and_root import \
    CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer
from bodzify_api.serializer.track.output.without_playlists_and_album_and_genre import \
    LibTrackWithoutAlbumPlaylistGenreSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    CREATED_ON = AttributesLabels.CREATED_ON
    UPDATED_ON = AttributesLabels.UPDATED_ON
    LIB_TRACKS = AttributesLabels.LIB_TRACKS
    LIB_TRACKS_TITLE = LibTrackAttributesLabels.TITLE
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_ARCHIVED_COUNT = AttributesLabels.LIB_TRACKS_ARCHIVED_COUNT
    TYPE = AttributesLabels.TYPE
    TYPE_LABEL = CriteriaTypeFields.LABEL
    ROOT = AttributesLabels.ROOT
    PARENT = AttributesLabels.PARENT
    ASCENDANTS = AttributesLabels.ASCENDANTS
    DESCENDANTS = AttributesLabels.DESCENDANTS
    CHILDREN = AttributesLabels.CHILDREN
    CRITERIA_PLAYLIST = AttributesLabels.CRITERIA_PLAYLIST


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackWithoutAlbumPlaylistGenreSerializer(
        source=AttributesLabels.LIB_TRACKS_NOT_ARCHIVED, many=True)
    type = CriteriaTypeSerializer()
    root = CriteriaSimpleSerializer()  # type: ignore
    parent = CriteriaSimpleSerializer()
    ascendants = CriteriaAscendantRelationWithoutDescendantSerializer(
        source=AttributesLabels.CRITERIA_ASCENDANT_RELATION_ASCENDANTS,
        many=True)
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=AttributesLabels.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)
    children = serializers.SerializerMethodField()
    criteria_playlist = CriteriaPlaylistWithoutCriteriaAndTracksAndParentAndRootSerializer()

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.PARENT,
                  Fields.ASCENDANTS,
                  Fields.DESCENDANTS,
                  Fields.ROOT,
                  Fields.CHILDREN,
                  Fields.TYPE,
                  Fields.CREATED_ON,
                  Fields.CRITERIA_PLAYLIST,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,]

    def get_children(self, obj) -> List[Dict[str, Any]]:
        return CriteriaSimpleSerializer(obj.get_children(), many=True).data  # type: ignore
