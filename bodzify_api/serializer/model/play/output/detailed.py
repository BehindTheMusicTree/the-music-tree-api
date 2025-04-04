from typing import Any

from rest_framework import serializers

from bodzify_api.model.play.Play import Play
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.field.AppCharField import AppCharField
from bodzify_api.serializer.model.uploaded_track.output.detailed import UploadedTrackDetailedSerializer
from bodzify_api.serializer.model.playlist.base.output.detailed import PlaylistDetailedSerializer

from .Fields import Fields


class PlayDetailedSerializer(serializers.ModelSerializer):
    content_type = AppCharField(source=f'{Fields.CONTENT_TYPE}.model')
    content = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = [Fields.UUID,
                  Fields.CONTENT_TYPE,
                  Fields.CONTENT,
                  Fields.CREATED_ON]

    def get_content(self, obj: Play) -> list | Any | dict:
        if isinstance(obj.content, Playlist):
            return PlaylistDetailedSerializer(obj.content).data
        else:
            return UploadedTrackDetailedSerializer(obj.content).data
