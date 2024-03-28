#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer import LibTrackDetailedSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    RELATIVE_URL = ATTRIBUTES_LABEL.RELATIVE_URL
    FILENAME = ATTRIBUTES_LABEL.FILENAME
    FILE_EXTENSION = ATTRIBUTES_LABEL.FILE_EXTENSION
    TITLE = ATTRIBUTES_LABEL.TITLE
    ARTIST = ATTRIBUTES_LABEL.ARTIST
    ALBUM = ATTRIBUTES_LABEL.ALBUM
    DURATION = ATTRIBUTES_LABEL.DURATION
    RATING = ATTRIBUTES_LABEL.RATING
    LANGUAGE = ATTRIBUTES_LABEL.LANGUAGE
    ADDED_ON = ATTRIBUTES_LABEL.ADDED_ON
    PLAY_COUNT = ATTRIBUTES_LABEL.PLAY_COUNT


class LibTrackWithoutPlaylistsAndGenreSerializer(LibTrackDetailedSerializer):

    class Meta:
        model = LibraryTrack
        fields = [
            FIELDS.UUID,
            FIELDS.RELATIVE_URL,
            FIELDS.FILENAME,
            FIELDS.FILE_EXTENSION,
            FIELDS.TITLE,
            FIELDS.ARTIST,
            FIELDS.ALBUM,
            FIELDS.DURATION,
            FIELDS.RATING,
            FIELDS.LANGUAGE,
            FIELDS.ADDED_ON,
            FIELDS.PLAY_COUNT,
            FIELDS.PLAY_COUNT
        ]
