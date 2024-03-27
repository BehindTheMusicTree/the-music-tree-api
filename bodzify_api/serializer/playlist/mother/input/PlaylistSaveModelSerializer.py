#!/usr/bin/env python

from bodzify_api.model.playlist.Playlist import ATTRIBUTES_LABEL as PLAYLIST_ATTRIBUTES_LABEL, Playlist
from rest_framework import serializers


class FIELDS:
    USER = PLAYLIST_ATTRIBUTES_LABEL.USER


class PlaylistSaveModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = [FIELDS.USER]
