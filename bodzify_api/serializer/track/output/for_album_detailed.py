#!/usr/bin/env python

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.album.with_only_name_and_artists import AlbumWithOnlyNameAndArtistsSerializer
from bodzify_api.serializer.artist.detailed import ArtistDetailedSerializer
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.criteria.output.simple import CriteriaSimpleSerializer
from bodzify_api.serializer.track.output.detailed import Fields as LibTrackDetailedFields
from bodzify_api.serializer.track.output.detailed import LibTrackDetailedSerializer


class Fields:
    POSITION_IN_ALBUM = LibTrackDetailedFields.POSITION_IN_ALBUM
    UUID = LibTrackDetailedFields.UUID
    TITLE = LibTrackDetailedFields.TITLE
    ARTISTS = LibTrackDetailedFields.ARTISTS
    GENRE = LibTrackDetailedFields.GENRE
    DURATION_STR_IN_HOUR_MIN_SEC = LibTrackDetailedFields.DURATION_STR_IN_HOUR_MIN_SEC
    RATING = LibTrackDetailedFields.RATING
    LANGUAGE = LibTrackDetailedFields.LANGUAGE


class LibTrackForAlbumDetailedSerializer(LibTrackDetailedSerializer):
    genre = CriteriaSimpleSerializer()
    artists = ArtistWithOnlyNameSerializer(many=True)

    class Meta:
        model = LibraryTrack
        fields = [Fields.POSITION_IN_ALBUM,
                  Fields.UUID,
                  Fields.TITLE,
                  Fields.ARTISTS,
                  Fields.GENRE,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.RATING,
                  Fields.LANGUAGE,]
