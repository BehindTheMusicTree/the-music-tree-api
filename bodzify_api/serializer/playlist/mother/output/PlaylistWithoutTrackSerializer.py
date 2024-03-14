#!/usr/bin/env python

from lib2to3.fixes.fix_idioms import TYPE
from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL, Playlist
from bodzify_api.model.playlist.children.SimplePlaylist import TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    TYPE = ATTRIBUTES_LABEL.TYPE
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    LIBRARY_TRACKS_COUNT = ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT


class PlaylistWithoutTrackSerializer(serializers.ModelSerializer):
    library_tracks_count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    def get_library_tracks_count(self, obj):
        return obj.library_tracks.count()

    def get_name(self, obj):
        if hasattr(obj, ATTRIBUTES_LABEL.CRITERIA_PLAYLIST):
            return obj.criteria_playlist.name
        elif hasattr(obj, ATTRIBUTES_LABEL.SIMPLE_PLAYLIST):
            return obj.simple_playlist.name
        else:
            return None

    def get_type(self, obj):
        if hasattr(obj, ATTRIBUTES_LABEL.CRITERIA_PLAYLIST):
            return obj.criteria_playlist.type.label
        elif hasattr(obj, ATTRIBUTES_LABEL.SIMPLE_PLAYLIST):
            return SIMPLE_PLAYLIST_TYPE_LABEL
        else:
            return None

    class Meta:
        model = Playlist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.TYPE,
                  FIELDS.ADDED_ON,
                  FIELDS.LIBRARY_TRACKS_COUNT]
