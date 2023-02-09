#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.TrackDetailedSerializer import (
    TrackDetailedSerializer)

class TrackWithoutPlaylistsSerializer(TrackDetailedSerializer):

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
            "addedOn"
        ]
