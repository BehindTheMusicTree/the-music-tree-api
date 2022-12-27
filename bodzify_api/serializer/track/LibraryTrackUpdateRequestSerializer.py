#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.CriteriaSerializer import CriteriaResponseSerializer
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)


class LibraryTrackUpdateRequestSerializer(serializers.ModelSerializer):

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
