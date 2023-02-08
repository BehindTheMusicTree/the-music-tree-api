#!/usr/bin/env python

from django.db.models import Sum
from rest_framework import serializers

from bodzify_api.model.Album import Album
from bodzify_api.model.track.LibraryTrack import LibraryTrack


class AlbumWithNameAndMetaSerializer(serializers.ModelSerializer):
    trackCount = serializers.IntegerField(source='librarytrack_set.count')
    duration = serializers.SerializerMethodField()

    def get_duration(self, obj):
        value = LibraryTrack.objects.filter(album=obj).aggregate(duration=Sum('duration'))
        return value['duration']

    class Meta:
        model = Album
        fields = [
            'uuid',
            'name',
            'year',
            'trackCount',
            'duration']
