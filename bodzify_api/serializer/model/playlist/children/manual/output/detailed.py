
from rest_framework import serializers

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.model.lib_track.output.simple.simple_without_album \
    import LibTrackSimpleWithoutPlaylistAndAlbumSerializer
from .Fields import Fields


class ManualPlaylistDetailedSerializer(serializers.ModelSerializer):
    library_tracks_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks = LibTrackSimpleWithoutPlaylistAndAlbumSerializer(
        source=Fields.LIB_TRACKS_NOT_ARCHIVED_INTERNAL, many=True)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    name = AppCharField()

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.LIB_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
