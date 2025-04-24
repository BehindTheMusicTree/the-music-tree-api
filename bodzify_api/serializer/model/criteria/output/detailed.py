from rest_framework import serializers
from rest_framework.fields import IntegerField

from bodzify_api.model.criteria.Criteria import Criteria
from bodzify_api.model.criteria.Fields import Fields as ModelFields
from bodzify_api.serializer.AppSerializer import AppSerializer
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.model.criteria_lineage_rel.without_ascendant import (
    CriteriaLineageRelWithoutAscendantSerializer
)
from bodzify_api.serializer.model.criteria_lineage_rel.without_descendant import (
    CriteriaLineageRelWithoutDescendantSerializer
)
from bodzify_api.serializer.model.uploaded_track.output.simple.simple_without_album_and_genre import (
    UploadedTrackWithoutAlbumPlaylistGenreSerializer
)
from bodzify_api.serializer.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer

from .Fields import Fields as Fields
from .minimum import CriteriaMinimumSerializer


class CriteriaDetailedSerializer(AppSerializer, serializers.ModelSerializer):
    uploaded_tracks = UploadedTrackWithoutAlbumPlaylistGenreSerializer(
        source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL, many=True)
    uploaded_tracks_count = IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    uploaded_tracks_archived_count = IntegerField(source=Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_INTERNAL)
    parent = CriteriaMinimumSerializer()
    ascendants = CriteriaLineageRelWithoutDescendantSerializer(source=ModelFields.ASCENDANTS_RELS, many=True)
    descendants = CriteriaLineageRelWithoutAscendantSerializer(source=ModelFields.DESCENDANTS_RELS, many=True)
    root = CriteriaMinimumSerializer()  # type: ignore
    children = CriteriaMinimumSerializer(many=True)
    criteria_playlist = CriteriaPlaylistMinimumSerializer()
    name = AppCharField(source=ModelFields.NAME_INTERNAL)

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
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]
