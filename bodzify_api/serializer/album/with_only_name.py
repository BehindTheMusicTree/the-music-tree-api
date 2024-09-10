#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ATTRIBUTES_LABEL


class AlbumWithOnlyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = [ATTRIBUTES_LABEL.UUID, ATTRIBUTES_LABEL.NAME]
