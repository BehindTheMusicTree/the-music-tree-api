#!/usr/bin/env python

import datetime
from typing import Any, Dict, List, cast
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.serializer.album.without_tracks import AlbumWithoutTracksSerializer
from bodzify_api.model.Artist import Artist, AttributesLabels
from bodzify_api.serializer.track.output.without_playlists_and_artist import LibTrackWithoutArtistAndPlaylistSerializer


class Fields:
    UUID = AttributesLabels.UUID
    NAME = AttributesLabels.NAME
    ALBUMS = AttributesLabels.ALBUMS
    LIB_TRACKS = AttributesLabels.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabels.LIB_TRACKS_COUNT
    DURATION_IN_SEC = AttributesLabels.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabels.DURATION_STR_IN_HOUR_MIN_SEC
    LIB_TRACKS_COUNT_ARCHIVED = AttributesLabels.LIB_TRACKS_COUNT_ARCHIVED


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumWithoutTracksSerializer(many=True)
    library_tracks = LibTrackWithoutArtistAndPlaylistSerializer(
        source=AttributesLabels.LIB_TRACKS_NOT_ARCHIVED, many=True)

    class Meta:
        model = Artist
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.ALBUMS,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.LIB_TRACKS_COUNT_ARCHIVED,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,
                  Fields.LIB_TRACKS_COUNT_ARCHIVED]
