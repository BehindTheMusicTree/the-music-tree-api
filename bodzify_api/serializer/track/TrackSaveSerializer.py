#!/usr/bin/env python
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class TrackSaveSerializer(InputModelSerializer):

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
        
