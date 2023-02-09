#!/usr/bin/env python

from django.db.models import Sum
from rest_framework import serializers

from bodzify_api.serializer.album.AlbumWithoutTracksSerializer import AlbumWithoutTracksSerializer
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumWithoutTracksSerializer(source='album_set', many=True)
    trackCount = serializers.IntegerField(source='librarytrack_set.count')
    duration = serializers.SerializerMethodField()
  
    def get_duration(self, obj) -> float:
        value = LibraryTrack.objects.filter(artist=obj).aggregate(duration=Sum('duration'))
        return value['duration']

    class Meta:
        model = Artist
        fields = ['uuid', 'name', 'albums', 'trackCount', 'duration']
