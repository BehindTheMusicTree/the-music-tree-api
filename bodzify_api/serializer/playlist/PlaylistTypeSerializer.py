#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.PlaylistType import PlaylistType


class PlaylistTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlaylistType
        fields = ["label"]
