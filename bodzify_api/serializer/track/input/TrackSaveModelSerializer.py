#!/usr/bin/env python
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.InputModelSerializer import InputModelSerializer


class TrackSaveModelSerializer(InputModelSerializer):

    class Meta:
        model = LibraryTrack
        fields = [
            LibraryTrack.ATTRIBUTE_USER_LABEL,
            LibraryTrack.ATTRIBUTE_FILE_LABEL,
            LibraryTrack.ATTRIBUTE_TITLE_LABEL, 
            LibraryTrack.ATTRIBUTE_ARTIST_LABEL,
            LibraryTrack.ATTRIBUTE_ALBUM_LABEL, 
            LibraryTrack.ATTRIBUTE_GENRE_LABEL,
            LibraryTrack.ATTRIBUTE_DURATION_LABEL,
            LibraryTrack.ATTRIBUTE_RATING_LABEL, 
            LibraryTrack.ATTRIBUTE_LANGUAGE_LABEL,
        ]
        
