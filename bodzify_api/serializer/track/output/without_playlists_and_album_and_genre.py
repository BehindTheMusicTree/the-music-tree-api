#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer, Fields as LibTrackDetailedFields


class Fields:
    UUID = LibTrackDetailedFields.UUID
    RELATIVE_URL = LibTrackDetailedFields.RELATIVE_URL
    FILE = LibTrackDetailedFields.FILE
    TITLE = LibTrackDetailedFields.TITLE
    ARTIST = LibTrackDetailedFields.ARTIST
    DURATION_IN_SEC = LibTrackDetailedFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackDetailedFields.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = LibTrackDetailedFields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE
    MUSICBRAINZ_RECORDING = LibTrackDetailedFields.MUSICBRAINZ_RECORDING
    RATING = LibTrackDetailedFields.RATING
    LANGUAGE = LibTrackDetailedFields.LANGUAGE
    CREATED_ON = LibTrackDetailedFields.CREATED_ON
    PLAY_COUNT = LibTrackDetailedFields.PLAY_COUNT


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
