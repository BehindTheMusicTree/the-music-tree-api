#!/usr/bin/env python

from rest_framework import serializers

from bodzify_api.model.track.LibraryTrack import LibraryTrack
from bodzify_api.serializer.criteria.CriteriaSerializer import CriteriaResponseSerializer
from bodzify_api.serializer.artist.ArtistWithOnlyNameSerializer import ArtistWithOnlyNameSerializer
from bodzify_api.serializer.album.AlbumWithNameAndMetaSerializer import (
        AlbumWithNameAndMetaSerializer)
from bodzify_api.serializer.playlist.PlaylistWithoutTracksSerializer import (
    PlaylistWithoutTracksSerializer)

class TrackDetailedSerializer(serializers.ModelSerializer):
    genre = CriteriaResponseSerializer()
    artist = ArtistWithOnlyNameSerializer()
    album = AlbumWithNameAndMetaSerializer()
    playlists = PlaylistWithoutTracksSerializer(many=True)

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
            'album',
            'genre',
            'duration',
            'rating',
            'language',
            'playlists',
            'addedOn']
