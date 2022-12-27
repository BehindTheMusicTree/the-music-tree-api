#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.CriteriaSerializer import CriteriaResponseSerializer
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)

class LibraryTrackResponseSerializer(serializers.ModelSerializer):
    genre = CriteriaResponseSerializer()
    playlists = PlaylistWithoutTracksSerializer(many=True)

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
            "playlists",
            "addedOn"]
