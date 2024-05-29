#!/usr/bin/env python

from bodzify_api.model.Album import Album
from bodzify_api.serializer.endpoint import InputEndpointSerializer
from bodzify_api.serializer.album.input.model import ATTRIBUTES_LABEL as SAVE_MODEL_ATTRIBUTES_LABEL


class FIELDS:
    NAME = SAVE_MODEL_ATTRIBUTES_LABEL.NAME
    ALBUM_ARTISTS_STR = SAVE_MODEL_ATTRIBUTES_LABEL.ALBUM_ARTISTS + "_string"


class AlbumSaveSchemaSerializer(InputEndpointSerializer):

    class Meta:
        model = Album
        fields = [FIELDS.NAME,
                  FIELDS.ALBUM_ARTISTS_STR]
