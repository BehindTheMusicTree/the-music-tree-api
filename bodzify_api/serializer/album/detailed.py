#!/usr/bin/env python

import datetime
from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.utils import utils
from bodzify_api.model.Album import Album, AttributesLabel as AttributesLabel
from bodzify_api.model.track.LibraryTrack import LibraryTrack, AttributesLabel as LIB_TRACK_ATTRIBUTES_LABEL
from bodzify_api.serializer.track.output.without_playlists_and_album import (
    LibTrackWithoutAlbumAndPlaylistSerializer)
from bodzify_api.serializer.artist.with_only_name import ArtistWithOnlyNameSerializer


class Fields:
    UUID = AttributesLabel.UUID
    NAME = AttributesLabel.NAME
    YEAR = AttributesLabel.YEAR
    ALBUM_ARTISTS = AttributesLabel.ALBUM_ARTISTS
    LIB_TRACKS = AttributesLabel.LIB_TRACKS
    LIB_TRACKS_COUNT = AttributesLabel.LIB_TRACKS_COUNT
    DURATION_IN_SEC = AttributesLabel.DURATION_IN_SEC
    DURATION_STR_IN_HOUR_MIN_SEC = AttributesLabel.DURATION_STR_IN_HOUR_MIN_SEC


class AlbumDetailedSerializer(serializers.ModelSerializer):
    library_tracks_count = serializers.IntegerField(source=AttributesLabel.LIB_TRACKS + '.count')
    library_tracks = LibTrackWithoutAlbumAndPlaylistSerializer(many=True)
    album_artists = ArtistWithOnlyNameSerializer(many=True)
    duration_in_sec = serializers.SerializerMethodField()
    duration_str_in_hour_min_sec = serializers.SerializerMethodField()

    def get_duration_in_sec(self, obj) -> int:
        value = LibraryTrack.objects.filter(album=obj).aggregate(duration_in_sec=Sum(AttributesLabel.DURATION_IN_SEC))
        return value[LIB_TRACK_ATTRIBUTES_LABEL.DURATION_IN_SEC]

    def get_duration_str_in_hour_min_sec(self, obj) -> str:
        return str(datetime.timedelta(seconds=self.get_duration_in_sec(obj)))

    class Meta:
        model = Album
        fields = [Fields.UUID,
                  Fields.NAME,
                  Fields.YEAR,
                  Fields.ALBUM_ARTISTS,
                  Fields.LIB_TRACKS,
                  Fields.LIB_TRACKS_COUNT,
                  Fields.DURATION_IN_SEC,
                  Fields.DURATION_STR_IN_HOUR_MIN_SEC,]
