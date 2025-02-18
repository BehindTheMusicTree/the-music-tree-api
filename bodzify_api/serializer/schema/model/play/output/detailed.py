from typing import Any
from typing import Dict
from typing import List

from rest_framework import serializers

from bodzify_api.model.play.Play import Play
from bodzify_api.model.playlist.Playlist import Playlist
from bodzify_api.serializer.schema.model.lib_track.output.simple.simple_without_album_and_genre import \
    LibTrackWithoutAlbumPlaylistGenreSerializer
from bodzify_api.serializer.schema.model.playlist.base.output.detailed import PlaylistDetailedSerializer
from .Fields import Fields


class PlayDetailedSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source=f'{Fields.CONTENT_TYPE}.model')
    content = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = [Fields.UUID,
                  Fields.CONTENT_TYPE,
                  Fields.CONTENT,
                  Fields.CREATED_ON]

    def get_content_object(self, obj: Play) -> List | Any | Dict:
        if isinstance(obj.content, Playlist):
            return PlaylistDetailedSerializer(obj.content).data
        else:
            return LibTrackWithoutAlbumPlaylistGenreSerializer(obj.content).data
