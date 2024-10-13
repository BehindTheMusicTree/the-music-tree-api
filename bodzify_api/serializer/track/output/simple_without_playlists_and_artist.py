#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.album.with_only_name_and_artists import AlbumWithOnlyNameAndArtistsSerializer
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.track.output.detailed import Fields as LibTrackDetailedFields
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer


class Fields:
    UUID = LibTrackDetailedFields.UUID
    RELATIVE_URL = LibTrackDetailedFields.RELATIVE_URL
    FILE = LibTrackDetailedFields.FILE
    TITLE = LibTrackDetailedFields.TITLE
    ALBUM = LibTrackDetailedFields.ALBUM
    POSITION_IN_ALBUM = LibTrackDetailedFields.POSITION_IN_ALBUM
    GENRE = LibTrackDetailedFields.GENRE
    DURATION_IN_SEC = LibTrackDetailedFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackDetailedFields.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING = LibTrackDetailedFields.MUSICBRAINZ_RECORDING
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = LibTrackDetailedFields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE
    RATING = LibTrackDetailedFields.RATING
    LANGUAGE = LibTrackDetailedFields.LANGUAGE
    PLAY_COUNT = LibTrackDetailedFields.PLAY_COUNT


class LibTrackSimpleWithoutPlaylistAndArtistSerializer(LibTrackDetailedSerializer):
    genre = CriteriaSimpleSerializer()
    album = AlbumWithOnlyNameAndArtistsSerializer()

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.TITLE,
                  Fields.ALBUM,
                  Fields.GENRE,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.RATING,
                  Fields.LANGUAGE,]
