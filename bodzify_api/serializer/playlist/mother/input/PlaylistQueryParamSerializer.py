#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.playlist.children.CriteriaPlaylist import TYPES_LABEL as CRITERIA_PLAYLIST_TYPES_LABEL
from bodzify_api.model.playlist.children.SimplePlaylist import TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL


class FIELDS:
    TYPE = 'type'
    NAME = PLAYLIST_ATTRIBUTES_LABEL.NAME


class PlaylistQueryParamSerializer(serializers.Serializer):
    type = serializers.CharField(required=False)
    name = serializers.CharField(required=False, allow_blank=True)

    def validate_type(self, value):
        valid_types = [CRITERIA_PLAYLIST_TYPES_LABEL.GENRE,
                       CRITERIA_PLAYLIST_TYPES_LABEL.TAG,
                       SIMPLE_PLAYLIST_TYPE_LABEL]
        if value not in valid_types:
            raise serializers.ValidationError("Invalid type.")
        return value
