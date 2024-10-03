#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.playlist.children.CriteriaPlaylist import TypesLabel as CriteriaPlaylistTypesLabels
from bodzify_api.model.playlist.children.SimplePlaylist import TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL
from bodzify_api.model.playlist.BasePlaylist import AttributesLabels as PlaylistAttributesLabels


class Fields:
    TYPE = 'type'
    NAME = PlaylistAttributesLabels.NAME


class BasePlaylistQueryParamSerializer(serializers.Serializer):
    TYPE_VALID_VALUES = [CriteriaPlaylistTypesLabels.GENRE,
                         CriteriaPlaylistTypesLabels.TAG,
                         SIMPLE_PLAYLIST_TYPE_LABEL]

    type = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)

    def validate_type(self, value):
        if value not in self.TYPE_VALID_VALUES:
            raise serializers.ValidationError(
                {Fields.TYPE: ["Invalid type. Valid values are: " + ", ".join(self.TYPE_VALID_VALUES)]})
        return value

    def validate_name(self, value):
        if value == '':
            raise serializers.ValidationError({Fields.NAME: "Name cannot be empty"})
        return value
