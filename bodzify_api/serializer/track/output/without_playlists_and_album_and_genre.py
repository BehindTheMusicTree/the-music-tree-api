#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer, Fields as LIB_TRACK_DetailedFields


class Fields:
    UUID = LIB_TRACK_DetailedFields.UUID
    RELATIVE_URL = LIB_TRACK_DetailedFields.RELATIVE_URL
    FILE = LIB_TRACK_DetailedFields.FILE
    TITLE = LIB_TRACK_DetailedFields.TITLE
    ARTIST = LIB_TRACK_DetailedFields.ARTIST
    DURATION_IN_SEC = LIB_TRACK_DetailedFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LIB_TRACK_DetailedFields.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = LIB_TRACK_DetailedFields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE
    MUSICBRAINZ_RECORDING = LIB_TRACK_DetailedFields.MUSICBRAINZ_RECORDING
    RATING = LIB_TRACK_DetailedFields.RATING
    LANGUAGE = LIB_TRACK_DetailedFields.LANGUAGE
    CREATED_ON = LIB_TRACK_DetailedFields.CREATED_ON
    PLAY_COUNT = LIB_TRACK_DetailedFields.PLAY_COUNT


class LibTrackWithoutAlbumPlaylistGenreSerializer(LibTrackDetailedSerializer):
    artist = ArtistWithOnlyNameSerializer()

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.RELATIVE_URL,
                  Fields.FILE,
                  Fields.TITLE,
                  Fields.ARTIST,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.MUSICBRAINZ_RECORDING,
                  Fields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.CREATED_ON,
                  Fields.PLAY_COUNT]
