from typing import Any
from typing import Dict as ReturnDict
from typing import List as ReturnList

from rest_framework import serializers

from bodzify_api.model.play.Play import Play
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.schema.model.lib_track.output.simple.simple_without_album_and_genre import \
    LibTrackWithoutAlbumPlaylistGenreSerializer
from bodzify_api.serializer.schema.model.playlist.base.output.detailed import PlaylistDetailedSerializer
from .Fields import Fields


class PlayDetailedSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type.model')
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = [Fields.UUID,
                  Fields.CONTENT_TYPE,
                  Fields.CONTENT_OBJECT,
                  Fields.CREATED_ON]

    def get_content_object(self, obj: Play) -> ReturnList | Any | ReturnDict:
        if isinstance(obj.content_object, Playlist):
            return PlaylistDetailedSerializer(obj.content_object).data
        else:
            return LibTrackWithoutAlbumPlaylistGenreSerializer(obj.content_object).data
