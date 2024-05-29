#!/usr/bin/env python

from bodzify_api.model.Album import ATTRIBUTES_LABEL, Album
from bodzify_api.serializer.endpoint import InputEndpointSerializer


class FIELDS:
    NAME = ATTRIBUTES_LABEL.NAME
    ALBUM_ARTISTS = ATTRIBUTES_LABEL.ALBUM_ARTISTS


class AlbumModelSerializer(InputEndpointSerializer):

    class Meta:
        model = Album
        fields = [FIELDS.NAME,
                  FIELDS.ALBUM_ARTISTS]
