
from rest_framework import serializers

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.model.lib_track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer
from .Fields import Fields


class ManualPlaylistDetailedSerializer(serializers.ModelSerializer):
    library_tracks = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(many=True)
    name = serializers.CharField()

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
