#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.Artist import Artist, AttributesLabels
from bodzify_api.serializer.album.with_only_name_and_artists import AlbumWithOnlyNameAndArtistsSerializer
from bodzify_api.serializer.track.output.simple_without_playlists_and_artist import LibTrackSimpleWithoutPlaylistAndArtistSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    ALBUMS = AttributesLabels.ALBUMS
    LIB_TRACKS = AttributesLabels.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    LIB_TRACKS_ARCHIVED_COUNT = AttributesLabels.LIB_TRACKS_ARCHIVED_COUNT


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumWithOnlyNameAndArtistsSerializer(many=True)
    library_tracks = LibTrackSimpleWithoutPlaylistAndArtistSerializer(
        source=AttributesLabels.LIB_TRACKS_NOT_ARCHIVED, many=True)

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUMS,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.LIB_TRACKS_ARCHIVED_COUNT]
