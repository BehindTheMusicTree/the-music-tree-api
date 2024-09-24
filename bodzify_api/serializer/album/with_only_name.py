#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.Album import Album, AttributesLabel as AttributesLabel


class AlbumWithOnlyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = [AttributesLabel.UUID, AttributesLabel.NAME]
