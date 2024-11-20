from rest_framework import serializers

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Fields import Fields as ModelFields
from bodzify_api.serializer.schema.model.criteria_lineage_rel.without_ascendant import CriteriaLineageRelWithoutAscendantSerializer
from bodzify_api.serializer.schema.model.criteria_lineage_rel.without_descendant import CriteriaLineageRelWithoutDescendantSerializer
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from bodzify_api.serializer.schema.model.lib_track.output.simple.simple_without_album_and_genre import \
    LibTrackWithoutAlbumPlaylistGenreSerializer
from .Fields import Fields as Fields
from .minimum import CriteriaMinimumSerializer


class CriteriaDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackWithoutAlbumPlaylistGenreSerializer(many=True)
    parent = CriteriaMinimumSerializer()
    ascendants = CriteriaLineageRelWithoutDescendantSerializer(source=ModelFields.ASCENDANTS_RELS, many=True)
    descendants = CriteriaLineageRelWithoutAscendantSerializer(source=ModelFields.DESCENDANTS_RELS, many=True)
    root = CriteriaMinimumSerializer()  # type: ignore
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
