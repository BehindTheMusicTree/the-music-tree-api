#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ALBUM_ATTRIBUTES_LABEL


class AlbumWithOnlyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = [
            ALBUM_ATTRIBUTES_LABEL.UUID, 
            ALBUM_ATTRIBUTES_LABEL.NAME
        ]
