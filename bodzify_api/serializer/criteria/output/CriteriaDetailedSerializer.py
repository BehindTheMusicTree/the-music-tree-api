#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria, ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import ATTRIBUTES_LABEL as LIBRARY_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.criteria.output.CriteriaSimpleSerializer import CriteriaSimpleSerializer
from bodzify_api.serializer.criteria.type.CriteriaTypeSerializer \
    import CriteriaTypeSerializer, FIELDS as CRITERIA_TYPE_FIELDS
from bodzify_api.serializer.criteria_ascendant_relation.detailed import CriteriaAscendantRelationDetailedSerializer
from bodzify_api.serializer.playlist.children.criteria.output.CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer import CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer

from bodzify_api.serializer.track.output.LibTrackWithoutAlbumPlaylistGenreSerializer \
    import LibTrackWithoutAlbumPlaylistGenreSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    PARENT = ATTRIBUTES_LABEL.PARENT
    ASCENDANTS = ATTRIBUTES_LABEL.ASCENDANTS
    ROOT = ATTRIBUTES_LABEL.ROOT
    CHILDREN = ATTRIBUTES_LABEL.CHILDREN
    TYPE = ATTRIBUTES_LABEL.TYPE
    TYPE_LABEL = CRITERIA_TYPE_FIELDS.LABEL
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    LIB_TRACKS = ATTRIBUTES_LABEL.LIB_TRACKS
    LIB_TRACKS_TITLE = LIBRARY_TRACK_ATTRIBUTES_LABEL.TITLE
    CRITERIA_PLAYLIST = ATTRIBUTES_LABEL.CRITERIA_PLAYLIST


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    type = CriteriaTypeSerializer()
    parent = CriteriaSimpleSerializer()
    ascendants = CriteriaAscendantRelationDetailedSerializer(
        source=ATTRIBUTES_LABEL.CRITERIA_ASCENDANT_RELATION_ASCENDANTS,
        many=True)
    ascendants = CriteriaAscendantRelationDetailedSerializer(
        source=ATTRIBUTES_LABEL.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)
    root = CriteriaSimpleSerializer()  # type: ignore
    children = serializers.SerializerMethodField()
    criteria_playlist = CriteriaPlaylistWithoutCriteriaTracksParentRootSerializer()
    library_tracks = LibTrackWithoutAlbumPlaylistGenreSerializer(many=True)

    class Meta:
        model = Criteria
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.PARENT,
                  FIELDS.ASCENDANTS,
                  FIELDS.ROOT,
                  FIELDS.CHILDREN,
                  FIELDS.TYPE,
                  FIELDS.ADDED_ON,
                  FIELDS.LIB_TRACKS,
                  FIELDS.CRITERIA_PLAYLIST]

    def get_children(self, obj):
        return CriteriaSimpleSerializer(obj.get_children(), many=True).data
