#!/usr/bin/env python

from typing import Any, Dict

from rest_framework import serializers

from bodzify_api.model.Play import Play, Fields as ModelFields
from bodzify_api.model.playlist.BasePlaylist import BasePlaylist
from bodzify_api.serializer.schema.playlist.base.output.detailed import BasePlaylistDetailedSerializer
from bodzify_api.serializer.schema.track.output.simple.simple_without_album_and_genre import \
    LibTrackWithoutAlbumPlaylistGenreSerializer


class Fields:
    CREATED_ON = ModelFields.CREATED_ON
    UPDATED_ON = ModelFields.UPDATED_ON
    CONTENT_TYPE = ModelFields.CONTENT_TYPE
    CONTENT_OBJECT = ModelFields.CONTENT_OBJECT


class PlayDetailedSerializer(serializers.ModelSerializer):
    content_type = serializers.CharField(source='content_type.model')
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Play
        fields = [Fields.CONTENT_TYPE,
                  Fields.CONTENT_OBJECT,
                  Fields.CREATED_ON,
                  Fields.UPDATED_ON]

    def get_content_object(self, obj) -> Dict[str, Any]:
        if isinstance(obj.content_object, BasePlaylist):
            return BasePlaylistDetailedSerializer(obj.content_object).data  # type: ignore
        else:
            return LibTrackWithoutAlbumPlaylistGenreSerializer(obj.content_object).data  # type: ignore
