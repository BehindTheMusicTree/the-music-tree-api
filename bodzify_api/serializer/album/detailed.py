#!/usr/bin/env python

from rest_framework import serializers
from bodzify_api.model.Album import Album, AttributesLabels
from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabels as LibTrackAttributesLabels
from bodzify_api.serializer.track.output.without_playlists_and_album import LibTrackWithoutAlbumAndPlaylistSerializer
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    YEAR = AttributesLabels.YEAR
    ALBUM_ARTISTS = AttributesLabels.ALBUM_ARTISTS
    LIB_TRACKS = AttributesLabels.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    LIB_TRACKS_COUNT_ARCHIVED = AttributesLabels.LIB_TRACKS_COUNT_ARCHIVED
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC


class AlbumDetailedSerializer(serializers.ModelSerializer):
    album_artists = ArtistWithOnlyNameSerializer(many=True)
    library_tracks = LibTrackWithoutAlbumAndPlaylistSerializer(
        source=AttributesLabels.LIB_TRACKS_NOT_ARCHIVED, many=True)

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_COUNT_ARCHIVED,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,]
