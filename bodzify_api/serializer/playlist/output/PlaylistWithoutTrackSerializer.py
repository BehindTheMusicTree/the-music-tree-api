#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL, Playlist


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    LIBRARY_TRACKS_COUNT = ATTRIBUTES_LABEL.LIBRARY_TRACKS_COUNT


class PlaylistWithoutTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.ADDED_ON]
