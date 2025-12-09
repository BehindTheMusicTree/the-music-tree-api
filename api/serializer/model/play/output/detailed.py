from typing import Any

from rest_framework import serializers

from api.model.play.Play import Play
from api.model.playlist.Playlist import Playlist
from api.serializer.field.AppCharField import AppCharField
from api.serializer.model.track.output.detailed import TrackDetailedSerializer
from api.serializer.model.playlist.base.output.detailed import PlaylistDetailedSerializer

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
            return TrackDetailedSerializer(obj.content).data
