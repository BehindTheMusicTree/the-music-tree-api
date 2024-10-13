#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.CriteriaPlaylist import \
    AttributesLabels as AttributesLabels


class Fields:
    NAME = AttributesLabels.NAME
    PARENT = AttributesLabels.PARENT


class CriteriaPlaylistQueryParamSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)
