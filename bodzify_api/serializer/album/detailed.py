#!/usr/bin/env python

import datetime
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.utils import utils
from bodzify_api.model.Album import Album, ATTRIBUTES_LABEL as ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack, ATTRIBUTES_LABEL as LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.output.without_playlists_and_album import (
    LibTrackWithoutAlbumAndPlaylistSerializer)
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer


class FIELDS:
    UUID = ATTRIBUTES_LABEL.UUID
    NAME = ATTRIBUTES_LABEL.NAME
    YEAR = ATTRIBUTES_LABEL.YEAR
    ALBUM_ARTISTS = ATTRIBUTES_LABEL.ALBUM_ARTISTS
    LIB_TRACKS = ATTRIBUTES_LABEL.LIB_TRACKS
    LIB_TRACKS_COUNT = ATTRIBUTES_LABEL.LIB_TRACKS_COUNT
    DURATION_IN_SEC = ATTRIBUTES_LABEL.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = ATTRIBUTES_LABEL.DURATION_STR_IN_HOUR_MIN_SEC


class AlbumDetailedSerializer(serializers.ModelSerializer):
    library_tracks_count = serializers.IntegerField(source=ATTRIBUTES_LABEL.LIB_TRACKS + '.count')
    library_tracks = LibTrackWithoutAlbumAndPlaylistSerializer(many=True)
    album_artists = ArtistWithOnlyNameSerializer(many=True)
    duration_in_sec = serializers.SerializerMethodField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    def get_duration_in_sec(self, obj) -> int:
        value = LibraryTrack.objects.filter(album=obj).aggregate(duration_in_sec=Sum(ATTRIBUTES_LABEL.DURATION_IN_SEC))
        return value[LIB_TRACK_ATTRIBUTES_LABEL.DURATION_IN_SEC]

    def get_duration_str_in_hour_min_sec(self, obj) -> str:
        return str(datetime.timedelta(seconds=self.get_duration_in_sec(obj)))

    class Meta:
        model = Album
        fields = [FIELDS.UUID,
                  FIELDS.NAME,
                  FIELDS.YEAR,
                  FIELDS.ALBUM_ARTISTS,
                  FIELDS.LIB_TRACKS,
                  FIELDS.LIB_TRACKS_COUNT,
                  FIELDS.DURATION_IN_SEC,
                  FIELDS.DURATION_STR_IN_HOUR_MIN_SEC,]
