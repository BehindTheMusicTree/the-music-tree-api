#!/usr/bin/env python

from typing import Optional
from rest_framework import serializers

from bodzify_api.model.playlist.BasePlaylist import AttributesLabel, BasePlaylist
from bodzify_api.model.playlist.children.SimplePlaylist import TYPE_LABEL as SIMPLE_PLAYLIST_TYPE_LABEL


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    TYPE = AttributesLabel.TYPE
    CREATED_ON = AttributesLabel.CREATED_ON
    LIB_TRACKS_COUNT = AttributesLabel.LIB_TRACKS_COUNT
    PLAY_COUNT = AttributesLabel.PLAY_COUNT
    LAST_TRACK_LIST_UPDATE_DATE = AttributesLabel.LAST_TRACK_LIST_UPDATE_DATE


class BasePlaylistWithoutTracksSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    library_tracks_count = serializers.IntegerField(source='f{AttributesLabel.LIB_TRACKS}.count', read_only=True)

    def get_name(self, obj) -> str:
        if hasattr(obj, AttributesLabel.CRITERIA_PLAYLIST):
            return obj.criteria_playlist.name
        elif hasattr(obj, AttributesLabel.SIMPLE_PLAYLIST):
            return obj.simple_playlist.name
        else:
            return None

    def get_type(self, obj) -> Optional[str]:
        if hasattr(obj, AttributesLabel.CRITERIA_PLAYLIST):
            return obj.criteria_playlist.type.label
        elif hasattr(obj, AttributesLabel.SIMPLE_PLAYLIST):
            return SIMPLE_PLAYLIST_TYPE_LABEL
        else:
            return None

    class Meta:
        model = BasePlaylist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.TYPE,
                  Fields.CREATED_ON,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.PLAY_COUNT,
                  Fields.LAST_TRACK_LIST_UPDATE_DATE]
