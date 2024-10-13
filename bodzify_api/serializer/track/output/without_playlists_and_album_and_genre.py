#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.artist.with_only_name import \
    ArtistWithOnlyNameSerializer
from bodzify_api.serializer.track.output.detailed import \
    Fields as LibTrackDetailedFields
from bodzify_api.serializer.track.output.detailed import \
    LibTrackDetailedSerializer


class Fields:
    UUID = LibTrackDetailedFields.UUID
    RELATIVE_URL = LibTrackDetailedFields.RELATIVE_URL
    FILE = LibTrackDetailedFields.FILE
    TITLE = LibTrackDetailedFields.TITLE
    ARTISTS = LibTrackDetailedFields.ARTISTS
    DURATION_IN_SEC = LibTrackDetailedFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackDetailedFields.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = LibTrackDetailedFields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE
    MUSICBRAINZ_RECORDING = LibTrackDetailedFields.MUSICBRAINZ_RECORDING
    RATING = LibTrackDetailedFields.RATING
    LANGUAGE = LibTrackDetailedFields.LANGUAGE
    PLAY_COUNT = LibTrackDetailedFields.PLAY_COUNT


class LibTrackWithoutAlbumPlaylistGenreSerializer(LibTrackDetailedSerializer):
    artists = ArtistWithOnlyNameSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.RELATIVE_URL,
                  Fields.FILE,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.MUSICBRAINZ_RECORDING,
                  Fields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAY_COUNT]
