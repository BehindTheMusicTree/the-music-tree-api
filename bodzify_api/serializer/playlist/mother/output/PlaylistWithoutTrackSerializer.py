#!/usr/bin/env python

from dbm.ndbm import library
from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL, Playlist


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    LIBRARY_TRACKS_COUNT = ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT


class PlaylistWithoutTrackSerializer(serializers.ModelSerializer):
    library_tracks_count = serializers.SerializerMethodField()

    def get_library_tracks_count(self, obj):
        return obj.library_tracks.count()

    class Meta:
        model = Playlist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON,
                  FIELDS.LIBRARY_TRACKS_COUNT]
