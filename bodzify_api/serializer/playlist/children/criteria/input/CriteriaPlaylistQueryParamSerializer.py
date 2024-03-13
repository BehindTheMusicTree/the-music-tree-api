#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.playlist.CriteriaPlaylist import ATTRIBUTES_LABEL as ATTRIBUTES_LABEL


class FIELDS:
    NAME = ATTRIBUTES_LABEL.NAME
    PARENT = ATTRIBUTES_LABEL.PARENT


class CriteriaPlaylistQueryParamSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)
