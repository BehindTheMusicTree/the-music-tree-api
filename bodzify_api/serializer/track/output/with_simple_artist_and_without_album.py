#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.output.detailed import CriteriaDetailedSerializer
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer, FIELDS as LIB_TRACK_DETAILED_FIELDS


class FIELDS:
    UUID = LIB_TRACK_DETAILED_FIELDS.UUID
    RELATIVE_URL = LIB_TRACK_DETAILED_FIELDS.RELATIVE_URL
    FILE = LIB_TRACK_DETAILED_FIELDS.FILE
    TITLE = LIB_TRACK_DETAILED_FIELDS.TITLE
    ARTIST = LIB_TRACK_DETAILED_FIELDS.ARTIST
    GENRE = LIB_TRACK_DETAILED_FIELDS.GENRE
    DURATION_IN_SEC = LIB_TRACK_DETAILED_FIELDS.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LIB_TRACK_DETAILED_FIELDS.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = LIB_TRACK_DETAILED_FIELDS.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE
    MUSICBRAINZ_RECORDING = LIB_TRACK_DETAILED_FIELDS.MUSICBRAINZ_RECORDING
    RATING = LIB_TRACK_DETAILED_FIELDS.RATING
    LANGUAGE = LIB_TRACK_DETAILED_FIELDS.LANGUAGE
    CREATED_ON = LIB_TRACK_DETAILED_FIELDS.CREATED_ON
    PLAY_COUNT = LIB_TRACK_DETAILED_FIELDS.PLAY_COUNT


class LibTrackWithoutAlbumAndSimpleArtistSerializer(LibTrackDetailedSerializer):
    genre = CriteriaDetailedSerializer()
    artist = ArtistWithOnlyNameSerializer()

    class Meta:
        model = LibraryTrack
        fields = [FIELDS.UUID,
                  FIELDS.RELATIVE_URL,
                  FIELDS.FILE,
                  FIELDS.TITLE,
                  FIELDS.ARTIST,
                  FIELDS.GENRE,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC,
                  FIELDS.MUSICBRAINZ_RECORDING,
                  FIELDS.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE,
                  FIELDS.RATING,
                  FIELDS.LANGUAGE,
                  FIELDS.CREATED_ON,
                  FIELDS.PLAY_COUNT]
