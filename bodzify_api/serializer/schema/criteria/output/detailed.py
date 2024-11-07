from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Fields import Fields as ModelFields
from bodzify_api.serializer.schema.criteria_ascendant_relation.without_ascendant import \
    CriteriaLineageRelationWithoutAscendantSerializer
from bodzify_api.serializer.schema.criteria_ascendant_relation.without_descendant import \
    CriteriaLineageRelationWithoutDescendantSerializer
from bodzify_api.serializer.schema.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from bodzify_api.serializer.schema.track.output.simple.simple_without_album_and_genre import \
    LibTrackWithoutAlbumPlaylistGenreSerializer
from .Fields import Fields as Fields
from .minimum import CriteriaMinimumSerializer


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackWithoutAlbumPlaylistGenreSerializer(many=True)
    root = CriteriaMinimumSerializer()  # type: ignore
    parent = CriteriaMinimumSerializer()
    ascendants = CriteriaLineageRelationWithoutDescendantSerializer(
        source=ModelFields.criteria_lineage_rel_ascendants,
        many=True)
    descendants = CriteriaLineageRelationWithoutAscendantSerializer(
        source=ModelFields.CRITERIA_ASCENDANT_RELATION_DESCENDANTS,
        many=True)
    children = CriteriaMinimumSerializer(many=True)
    criteria_playlist = CriteriaPlaylistMinimumSerializer()

    class Meta:
        model = Criteria
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.PARENT,
                  Fields.ASCENDANTS,
                  Fields.DESCENDANTS,
                  Fields.ROOT,
                  Fields.CHILDREN,
                  Fields.CRITERIA_PLAYLIST,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
