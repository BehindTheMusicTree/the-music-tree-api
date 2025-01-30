from rest_framework import serializers

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.model.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.schema.model.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from bodzify_api.serializer.schema.model.lib_track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer
from .Fields import Fields


class CriteriaPlaylistDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(
        source=Fields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL, many=True)
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_COUNT_INTERNAL)
    criteria = CriteriaMinimumSerializer()
    root = CriteriaPlaylistMinimumSerializer()  # type: ignore
    parent = CriteriaPlaylistMinimumSerializer()

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_PUBLIC,
                  Fields.LIB_TRACKS_COUNT_PUBLIC,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CRITERIA,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
