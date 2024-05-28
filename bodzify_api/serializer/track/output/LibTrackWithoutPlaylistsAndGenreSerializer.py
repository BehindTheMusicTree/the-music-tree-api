#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.track.output.LibTrackDetailedSerializer \
    import LibTrackDetailedSerializer, FIELDS as LIB_TRACK_DETAILED_FIELDS


class FIELDS:
    UUID = LIB_TRACK_DETAILED_FIELDS.UUID
    RELATIVE_URL = LIB_TRACK_DETAILED_FIELDS.RELATIVE_URL
    FILE = LIB_TRACK_DETAILED_FIELDS.FILE
    TITLE = LIB_TRACK_DETAILED_FIELDS.TITLE
    ARTIST = LIB_TRACK_DETAILED_FIELDS.ARTIST
    ALBUM = LIB_TRACK_DETAILED_FIELDS.ALBUM
    DURATION = LIB_TRACK_DETAILED_FIELDS.DURATION
    RATING = LIB_TRACK_DETAILED_FIELDS.RATING
    LANGUAGE = LIB_TRACK_DETAILED_FIELDS.LANGUAGE
    CREATED_ON = LIB_TRACK_DETAILED_FIELDS.CREATED_ON
    PLAY_COUNT = LIB_TRACK_DETAILED_FIELDS.PLAY_COUNT


class LibTrackWithoutPlaylistsAndGenreSerializer(LibTrackDetailedSerializer):

    class Meta:
        model = LibraryTrack
        fields = [
            FIELDS.UUID,
            FIELDS.RELATIVE_URL,
            FIELDS.FILE,
            FIELDS.TITLE,
            FIELDS.ARTIST,
            FIELDS.ALBUM,
            FIELDS.DURATION,
            FIELDS.RATING,
            FIELDS.LANGUAGE,
            FIELDS.CREATED_ON,
            FIELDS.PLAY_COUNT,
            FIELDS.PLAY_COUNT
        ]
