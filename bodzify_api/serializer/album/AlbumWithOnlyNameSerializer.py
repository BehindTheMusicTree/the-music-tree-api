#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.Album import Album


class AlbumWithOnlyNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['uuid', 'name']
