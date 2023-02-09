#!/usr/bin/env python

from django.db.models import Sum
from rest_framework import serializers

from bodzify_api.serializer.album.AlbumWithoutTracksAndArtistsSerializer import (
    AlbumWithoutTracksAndArtistsSerializer)
from bodzify_api.model.Artist import Artist
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class ArtistDetailedSerializer(serializers.ModelSerializer):
    albums = AlbumWithoutTracksAndArtistsSerializer(many=True)
    trackCount = serializers.IntegerField(source='librarytrack_set.count')
    duration = serializers.SerializerMethodField()
  
    def get_duration(self, obj):
        value = LibraryTrack.objects.filter(artist=obj).aggregate(duration=Sum('duration'))
        return value['duration']

    class Meta:
        model = Artist
        fields = ['uuid', 'name', 'albums', 'trackCount', 'duration']
