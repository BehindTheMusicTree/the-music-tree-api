#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class TrackSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [
            "user",
            "file",
            "title", 
            "artist", 
            "album", 
            "genre",
            "duration",
            "rating", 
            "language", 
        ]
