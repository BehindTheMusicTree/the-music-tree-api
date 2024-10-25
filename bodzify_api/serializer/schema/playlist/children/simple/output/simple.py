#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.children.ManualPlaylist import ManualPlaylist
from bodzify_api.serializer.schema.playlist.children.simple.output.detailed import Fields as AvailableFields


class Fields:
    UUID = AvailableFields.UUID
    NAME = AvailableFields.NAME
    LIB_TRACKS_COUNT = AvailableFields.LIB_TRACKS_COUNT


class ManualPlaylistSimpleSerializer(serializers.ModelSerializer):
    name = serializers.CharField()  # only to override the mother's one

    class Meta:
        model = ManualPlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.LIB_TRACKS_COUNT]
