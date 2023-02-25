#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TrackSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [
            "title", 
            "artist", 
            "album", 
            "genre", 
            "rating", 
            "language", 
        ]
