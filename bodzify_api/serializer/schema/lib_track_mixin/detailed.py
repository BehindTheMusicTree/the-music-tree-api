from rest_framework import serializers

from bodzify_api.model.lib_track_mixin.LibTrackMixin import LibTrackMixin
from bodzify_api.serializer.schema.lib_track.output.simple.simple_without_album_with_position_in_album \
    import LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer


class LibTrackMixinDetailedSerializer(serializers.ModelSerializer):
    library_tracks = serializers.SerializerMethodField()

    class Meta:
        model = LibTrackMixin

    def get_library_tracks(self, instance: LibTrackMixin):
        sorted_tracks = instance.lib_tracks_sorted
        return LibTrackSimpleWithoutAlbumWithPositionInAlbumSerializer(sorted_tracks, many=True).data
