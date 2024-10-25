#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.criteria.CriteriaPlaylist import \
    Fields as CriteriaPlaylistFields


class Fields:
    NAME = CriteriaPlaylistFields.NAME
    PARENT = CriteriaPlaylistFields.PARENT


class CriteriaPlaylistQueryParamSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    parent = serializers.CharField(required=False)
