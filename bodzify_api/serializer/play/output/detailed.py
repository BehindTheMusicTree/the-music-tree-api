#!/usr/bin/env python

from typing import Any, Dict
from bodzify_api.model.Play import Play, AttributesLabels
from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.serializer.playlist.base.output.with_tracks \
    import BasePlaylistWithTracksSerializer
from bodzify_api.serializer.track.output.without_playlists_and_album_and_genre \
    import LibTrackWithoutAlbumPlaylistGenreSerializer


class Fields:
    UUID = AttributesLabels.UUID
    CONTENT_TYPE = AttributesLabels.CONTENT_TYPE
    CONTENT_OBJECT = AttributesLabels.CONTENT_OBJECT
    TIME = AttributesLabels.TIME


class PlayDetailedSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type.model')
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = [Fields.UUID,
                  Fields.CONTENT_TYPE,
                  Fields.CONTENT_OBJECT,
                  Fields.TIME]

    def get_content_object(self, obj) -> Dict[str, Any]:
        if isinstance(obj.content_object, BasePlaylist):
            return BasePlaylistWithTracksSerializer(obj.content_object).data  # type: ignore
        else:
            return LibTrackWithoutAlbumPlaylistGenreSerializer(obj.content_object).data  # type: ignore
