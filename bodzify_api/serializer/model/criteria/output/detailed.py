from rest_framework import serializers
from rest_framework.fields import CharField, IntegerField

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Fields import Fields as ModelFields
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.model.criteria_lineage_rel.without_ascendant import (
    CriteriaLineageRelWithoutAscendantSerializer)
from bodzify_api.serializer.model.criteria_lineage_rel.without_descendant import (
    CriteriaLineageRelWithoutDescendantSerializer)
from bodzify_api.serializer.model.lib_track.output.simple.simple_without_album_and_genre import (
    LibTrackWithoutAlbumPlaylistGenreSerializer)
from bodzify_api.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer

from .Fields import Fields as Fields
from .minimum import CriteriaMinimumSerializer


class CriteriaDetailedSerializer(AppSerializer, serializers.ModelSerializer):
    library_tracks = LibTrackWithoutAlbumPlaylistGenreSerializer(
        source=Fields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL, many=True)
    library_tracks_count = IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks_archived_count = IntegerField(source=Fields.LIB_TRACKS_ARCHIVED_COUNT_INTERNAL)
    parent = CriteriaMinimumSerializer()
    ascendants = CriteriaLineageRelWithoutDescendantSerializer(source=ModelFields.ASCENDANTS_RELS, many=True)
    descendants = CriteriaLineageRelWithoutAscendantSerializer(source=ModelFields.DESCENDANTS_RELS, many=True)
    root = CriteriaMinimumSerializer()  # type: ignore
    children = CriteriaMinimumSerializer(many=True)
    criteria_playlist = CriteriaPlaylistMinimumSerializer()
    name = CharField(source=ModelFields.NAME_INTERNAL)

    class Meta:
        model = Criteria
        fields = [
            Fields.UUID,
            Fields.NAME,
            Fields.PARENT,
            Fields.ASCENDANTS,
            Fields.DESCENDANTS,
            Fields.ROOT,
            Fields.CHILDREN,
            Fields.CRITERIA_PLAYLIST,
            Fields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC,
            Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
            Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC,
            Fields.CREATED_ON,
            Fields.UPDATED_ON
        ]
