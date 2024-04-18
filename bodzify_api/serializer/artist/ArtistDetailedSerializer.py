#!/usr/bin/env python

from django.db.models import Sum
from rest_framework import serializers
from bodzify_api.serializer.album.output.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.model.Artist import Artist, ATTRIBUTES_LABEL
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumWithoutTracksSerializer(many=True)
    library_tracks_count = serializers.IntegerField(source=ATTRIBUTES_LABEL.LIB_TRACKS + '.count')
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj) -> float:
        value = LibraryTrack.objects.filter(artist=obj).aggregate(duration=Sum(ATTRIBUTES_LABEL.DURATION))
        return value[ATTRIBUTES_LABEL.DURATION]

    class Meta:
        model = Artist
        fields = [ATTRIBUTES_LABEL.UUID,
                  ATTRIBUTES_LABEL.NAME,
                  ATTRIBUTES_LABEL.ALBUMS,
                  ATTRIBUTES_LABEL.LIB_TRACKS,
                  ATTRIBUTES_LABEL.LIB_TRACKS_COUNT,
                  ATTRIBUTES_LABEL.DURATION]
