from rest_framework import serializers

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import CriteriaPlaylist
from bodzify_api.serializer.schema.playlist.children.criteria.output.Fields import Fields
from bodzify_api.serializer.schema.criteria.output.minimum import CriteriaMinimumSerializer
from bodzify_api.serializer.schema.playlist.children.criteria.output.minumum import CriteriaPlaylistMinimumSerializer
from bodzify_api.serializer.schema.lib_track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer


class CriteriaPlaylistDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(many=True)
    criteria = CriteriaMinimumSerializer()
    root = CriteriaPlaylistMinimumSerializer()  # type: ignore
    parent = CriteriaPlaylistMinimumSerializer()

    class Meta:
        model = CriteriaPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.CRITERIA,
                  Fields.PARENT,
                  Fields.ROOT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
