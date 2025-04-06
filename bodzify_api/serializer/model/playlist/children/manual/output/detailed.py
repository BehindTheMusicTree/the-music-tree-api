
from rest_framework import serializers

from bodzify_api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.model.uploaded_track.output.simple.simple_without_album import (
    UploadedTrackSimpleWithoutPlaylistAndAlbumSerializer
)

from .Fields import Fields


class ManualPlaylistDetailedSerializer(serializers.ModelSerializer):
    library_tracks_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    library_tracks = UploadedTrackSimpleWithoutPlaylistAndAlbumSerializer(
        source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_INTERNAL, many=True)
    library_tracks_archived_count = serializers.IntegerField(source=Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    name = AppCharField()

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.UPLOADED_TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.UPLOADED_TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
