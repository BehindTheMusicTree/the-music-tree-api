
from rest_framework import serializers

from api.model.playlist.children.manual.ManualPlaylist import ManualPlaylist
from api.serializer.field.AppCharField import AppCharField
from api.serializer.model.track.output.simple.simple_without_album import (
    TrackSimpleWithoutPlaylistAndAlbumSerializer
)

from .Fields import Fields


class ManualPlaylistDetailedSerializer(serializers.ModelSerializer):
    tracks_count = serializers.IntegerField(source=Fields.TRACKS_NOT_ARCHIVED_COUNT_INTERNAL)
    tracks = TrackSimpleWithoutPlaylistAndAlbumSerializer(
        source=Fields.TRACKS_NOT_ARCHIVED_INTERNAL, many=True)
    tracks_archived_count = serializers.IntegerField()
    name = AppCharField()

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TRACKS_NOT_ARCHIVED_PUBLIC,
                  Fields.TRACKS_NOT_ARCHIVED_COUNT_PUBLIC,
                  Fields.TRACKS_ARCHIVED_COUNT_PUBLIC,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON,]
