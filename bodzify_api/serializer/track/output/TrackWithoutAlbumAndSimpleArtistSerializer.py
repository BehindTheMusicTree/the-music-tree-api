#!/usr/bin/env python
from rest_framework import serializers
from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.output.CriteriaDetailedSerializer import CriteriaDetailedSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer


class TrackWithoutAlbumAndSimpleArtistSerializer(serializers.ModelSerializer):
    genre = CriteriaDetailedSerializer()
    artist = ArtistWithOnlyNameSerializer()

    class Meta:
        model = LibraryTrack
        fields = [
            'uuid',
            'relativeUrl',
            'filename',
            'fileExtension',
            'fileExists',
            'title',
            'artist',
            'genre',
            'duration',
            'rating',
            'language',
            'addedOn']
