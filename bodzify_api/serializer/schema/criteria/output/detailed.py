from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria, Fields as ModelFields
from bodzify_api.serializer.schema.criteria.output.fields import Fields as AvailableFields
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.schema.criteria.type.detailed import CriteriaTypeSerializer
from bodzify_api.serializer.schema.criteria_ascendant_relation.without_ascendant import \
    CriteriaAscendantRelationWithoutAscendantSerializer
from bodzify_api.serializer.schema.criteria_ascendant_relation.without_descendant import \
    CriteriaAscendantRelationWithoutDescendantSerializer
from bodzify_api.serializer.schema.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from bodzify_api.serializer.schema.track.output.simple.simple_without_album_and_genre import \
    LibTrackWithoutAlbumPlaylistGenreSerializer


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackWithoutAlbumPlaylistGenreSerializer(many=True)
    root = CriteriaMinimumSerializer()  # type: ignore
    parent = CriteriaMinimumSerializer()
    ascendants = CriteriaAscendantRelationWithoutDescendantSerializer(
        source=ModelFields.CRITERIA_ASCENDANT_RELATION_ASCENDANTS,
        many=True)
    descendants = CriteriaAscendantRelationWithoutAscendantSerializer(
        source=ModelFields.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)
    children = CriteriaMinimumSerializer(many=True)
    criteria_playlist = CriteriaPlaylistMinimumSerializer()

    class Meta:
        model = Criteria
        fields = [AvailableFields.UUID,
                  AvailableFields.NAME,
                  AvailableFields.PARENT,
                  AvailableFields.ASCENDANTS,
                  AvailableFields.DESCENDANTS,
                  AvailableFields.ROOT,
                  AvailableFields.CHILDREN,
                  AvailableFields.CRITERIA_PLAYLIST,
                  AvailableFields.LIB_TRACKS,
                  AvailableFields.LIB_TRACKS_COUNT,
                  AvailableFields.LIB_TRACKS_ARCHIVED_COUNT,
                  AvailableFields.CREATED_ON,
                  AvailableFields.UPDATED_ON,]
