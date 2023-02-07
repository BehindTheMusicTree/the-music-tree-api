#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.LibraryTrack import LibraryTrack


class LibraryTrackSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [
            'uuid',
            'relativeUrl',
            'filename',
            'fileExtension',
            "title", 
            "artist", 
            "album", 
            "genre", 
            "duration", 
            "rating", 
            "language", 
            "addedOn"]
