#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.album.detailed import AlbumDetailedSerializer
from bodzify_api.serializer.album.with_only_name import AlbumWithOnlyNameSerializer
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer, Fields as LibTrackDetailedFields


class Fields:
    UUID = LibTrackDetailedFields.UUID
    RELATIVE_URL = LibTrackDetailedFields.RELATIVE_URL
    FILE = LibTrackDetailedFields.FILE
    TITLE = LibTrackDetailedFields.TITLE
    ALBUM = LibTrackDetailedFields.ALBUM
    GENRE = LibTrackDetailedFields.GENRE
    DURATION_IN_SEC = LibTrackDetailedFields.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackDetailedFields.DURATION_STR_IN_HOUR_MIN_SEC
    MUSICBRAINZ_RECORDING = LibTrackDetailedFields.MUSICBRAINZ_RECORDING
    MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE = LibTrackDetailedFields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE
    RATING = LibTrackDetailedFields.RATING
    LANGUAGE = LibTrackDetailedFields.LANGUAGE
    PLAY_COUNT = LibTrackDetailedFields.PLAY_COUNT
    CREATED_ON = LibTrackDetailedFields.CREATED_ON


class LibTrackWithoutArtistAndPlaylistSerializer(LibTrackDetailedSerializer):
    genre = CriteriaSimpleSerializer()
    album = AlbumWithOnlyNameSerializer()

    class Meta:
        model = LibraryTrack
        fields = [Fields.UUID,
                  Fields.RELATIVE_URL,
                  Fields.FILE,
                  Fields.TITLE,
                  Fields.ALBUM,
                  Fields.GENRE,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.MUSICBRAINZ_RECORDING,
                  Fields.MUSICBRAINZ_RECORDING_LOOKUP_ERROR_CODE,
                  Fields.RATING,
                  Fields.LANGUAGE,
                  Fields.PLAY_COUNT,
                  Fields.CREATED_ON,]
