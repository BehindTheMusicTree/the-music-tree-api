#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.playlist.children.CriteriaPlaylist import AttributesLabel as AttributesLabel


class FIELDS:
    NAME = AttributesLabel.NAME
    PARENT = AttributesLabel.PARENT


class CriteriaPlaylistQueryParamSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)
