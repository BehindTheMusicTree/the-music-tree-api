#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import LibTrackDetailedSerializer


class LibTrackWithoutPlaylistsAndGenreSerializer(LibTrackDetailedSerializer):

    class Meta:
        model = LibraryTrack
        fields = [
            ATTRIBUTES_LABEL.UUID,
            ATTRIBUTES_LABEL.RELATIVE_URL,
            ATTRIBUTES_LABEL.FILENAME,
            ATTRIBUTES_LABEL.FILE_EXTENSION,
            ATTRIBUTES_LABEL.TITLE,
            ATTRIBUTES_LABEL.ARTIST,
            ATTRIBUTES_LABEL.ALBUM,
            ATTRIBUTES_LABEL.DURATION,
            ATTRIBUTES_LABEL.RATING,
            ATTRIBUTES_LABEL.LANGUAGE,
            ATTRIBUTES_LABEL.ADDED_ON]
